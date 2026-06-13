import json
from datetime import date
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg, Sum
from .models import Empleado
from .forms import EmpleadoForm
from planilla.models import RegistroPlanilla


@login_required
def dashboard_rrhh(request):
    hoy = date.today()
    primer_dia_mes = hoy.replace(day=1)

    total = Empleado.objects.count()
    activos = Empleado.objects.filter(estado='activo').count()
    inactivos = Empleado.objects.filter(estado='inactivo').count()
    nuevos_mes = Empleado.objects.filter(fecha_ingreso__gte=primer_dia_mes).count()
    avg_salario = (
        Empleado.objects.filter(estado='activo')
        .aggregate(Avg('salario'))['salario__avg'] or 0
    )

    por_depto = list(
        Empleado.objects.filter(estado='activo')
        .values('departamento__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')[:8]
    )

    por_contrato = list(
        Empleado.objects.filter(estado='activo')
        .values('tipo_contrato')
        .annotate(total=Count('id'))
    )
    CONTRATO_LABELS = {
        'indefinido': 'Indefinido',
        'plazo_fijo': 'Plazo Fijo',
        'honorarios': 'Honorarios',
        'pasantia':   'Pasantía',
    }
    for c in por_contrato:
        c['label'] = CONTRATO_LABELS.get(c['tipo_contrato'], c['tipo_contrato'])

    por_genero = list(
        Empleado.objects.filter(estado='activo')
        .values('genero')
        .annotate(total=Count('id'))
    )
    GENERO_LABELS = {'M': 'Masculino', 'F': 'Femenino', 'O': 'Otro'}
    for g in por_genero:
        g['label'] = GENERO_LABELS.get(g['genero'], g['genero'])

    ultimos = (
        Empleado.objects.select_related('departamento')
        .order_by('-fecha_ingreso')[:6]
    )

    # ── KPI 1: Tasa de Retención
    tasa_retencion = round(activos / total * 100, 1) if total else 0

    # ── KPI 2: Costo Total de Planilla Mensual
    MONTO_AF = Decimal('102.50')

    pl_mes = RegistroPlanilla.objects.filter(periodo=primer_dia_mes, empleado__estado='activo')
    costo_basico_mes = pl_mes.aggregate(s=Sum('sueldo_basico'))['s'] or Decimal('0')
    costo_mes = costo_basico_mes + pl_mes.filter(tiene_asignacion_familiar=True).count() * MONTO_AF

    primer_dia_mes_ant = (
        hoy.replace(month=hoy.month - 1, day=1) if hoy.month > 1
        else hoy.replace(year=hoy.year - 1, month=12, day=1)
    )
    pl_ant = RegistroPlanilla.objects.filter(periodo=primer_dia_mes_ant, empleado__estado='activo')
    costo_basico_ant = pl_ant.aggregate(s=Sum('sueldo_basico'))['s'] or Decimal('0')
    costo_ant = costo_basico_ant + pl_ant.filter(tiene_asignacion_familiar=True).count() * MONTO_AF

    hay_mes_anterior = costo_ant > 0
    variacion_planilla = (
        round(float(costo_mes - costo_ant) / float(costo_ant) * 100, 1)
        if hay_mes_anterior else 0
    )
    meta_planilla_ok = abs(variacion_planilla) <= 3 if hay_mes_anterior else None
    # Barra de progreso: escala ±10% → 0-100%
    planilla_bar = min(abs(variacion_planilla) / 10 * 100, 100) if hay_mes_anterior else 0
    costo_mes_display = f"{float(costo_mes):,.2f}"

    # ── KPI 3: Índice de Rotación (Turnover)
    turnover = round(inactivos / total * 100, 1) if total else 0

    return render(request, 'rrhh/dashboard.html', {
        'total':          total,
        'activos':        activos,
        'inactivos':      inactivos,
        'nuevos_mes':     nuevos_mes,
        'avg_salario':    avg_salario,
        'ultimos':        ultimos,
        'depto_labels':   json.dumps([d['departamento__nombre'] for d in por_depto]),
        'depto_data':     json.dumps([d['total'] for d in por_depto]),
        'contrato_labels': json.dumps([c['label'] for c in por_contrato]),
        'contrato_data':  json.dumps([c['total'] for c in por_contrato]),
        'genero_labels':  json.dumps([g['label'] for g in por_genero]),
        'genero_data':    json.dumps([g['total'] for g in por_genero]),
        # KPIs de gestión
        'tasa_retencion':    tasa_retencion,
        'costo_mes_display': costo_mes_display,
        'hay_mes_anterior':  hay_mes_anterior,
        'variacion_planilla': variacion_planilla,
        'meta_planilla_ok':  meta_planilla_ok,
        'planilla_bar':      round(planilla_bar, 1),
        'turnover':          turnover,
    })


@login_required
def lista_empleados(request):
    query = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')

    empleados = Empleado.objects.select_related('departamento').all()

    if query:
        empleados = empleados.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(cedula__icontains=query) |
            Q(cargo__icontains=query) |
            Q(departamento__nombre__icontains=query)
        )

    if estado in ('activo', 'inactivo'):
        empleados = empleados.filter(estado=estado)

    return render(request, 'rrhh/lista.html', {
        'empleados': empleados,
        'query': query,
        'estado': estado,
        'total': empleados.count(),
    })


@login_required
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save()
            messages.success(request, f'Empleado "{empleado.nombre_completo}" registrado.')
            return redirect('rrhh:empleados')
    else:
        form = EmpleadoForm()

    return render(request, 'rrhh/form.html', {'form': form, 'titulo': 'Nuevo Empleado'})


@login_required
def editar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, f'Empleado "{empleado.nombre_completo}" actualizado.')
            return redirect('rrhh:empleados')
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, 'rrhh/form.html', {
        'form': form, 'titulo': f'Editar: {empleado.nombre_completo}',
    })


@login_required
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == 'POST':
        nombre = empleado.nombre_completo
        empleado.delete()
        messages.success(request, f'Empleado "{nombre}" eliminado correctamente.')
        return redirect('rrhh:empleados')

    return render(request, 'rrhh/confirmar_eliminar.html', {'empleado': empleado})


@login_required
def detalle_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return render(request, 'rrhh/detalle.html', {'empleado': empleado})
