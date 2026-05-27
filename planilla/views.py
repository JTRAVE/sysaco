from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import RegistroPlanilla
from .forms import PlanillaForm, CalculadoraRapidaForm
from .calculadora import calcular_planilla_completa
from rrhh.models import Empleado


@login_required
def lista_planillas(request):
    planillas = RegistroPlanilla.objects.select_related('empleado', 'empleado__departamento').all()

    # Totales consolidados para el resumen
    resumen = []
    for p in planillas:
        calc = calcular_planilla_completa(p.sueldo_basico, p.tiene_asignacion_familiar, p.tipo_pension)
        resumen.append({
            'registro': p,
            'bruto': calc['remuneracion_bruta'],
            'descuentos': calc['total_descuentos'],
            'neto': calc['remuneracion_neta'],
            'essalud': calc['essalud'],
        })

    total_bruto = sum(r['bruto'] for r in resumen)
    total_descuentos = sum(r['descuentos'] for r in resumen)
    total_neto = sum(r['neto'] for r in resumen)
    total_essalud = sum(r['essalud'] for r in resumen)

    return render(request, 'planilla/lista.html', {
        'resumen': resumen,
        'total_bruto': total_bruto,
        'total_descuentos': total_descuentos,
        'total_neto': total_neto,
        'total_essalud': total_essalud,
    })


@login_required
def calculadora_rapida(request):
    resultado = None
    form = CalculadoraRapidaForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        sueldo = form.cleaned_data['sueldo_basico']
        tiene_familia = form.cleaned_data['tiene_asignacion_familiar']
        tipo_pension = form.cleaned_data['tipo_pension']
        resultado = calcular_planilla_completa(sueldo, tiene_familia, tipo_pension)

    return render(request, 'planilla/calculadora.html', {'form': form, 'resultado': resultado})


@login_required
def boleta_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == 'POST':
        sueldo = Decimal(request.POST.get('sueldo_basico', empleado.salario))
        tiene_familia = request.POST.get('tiene_asignacion_familiar') == 'on'
        tipo_pension = request.POST.get('tipo_pension', 'ONP')
    else:
        sueldo = empleado.salario
        tiene_familia = False
        tipo_pension = 'ONP'

    resultado = calcular_planilla_completa(sueldo, tiene_familia, tipo_pension)

    return render(request, 'planilla/boleta.html', {
        'empleado': empleado,
        'resultado': resultado,
        'tipo_pension': tipo_pension,
        'tiene_familia': tiene_familia,
    })


@login_required
def crear_registro(request):
    if request.method == 'POST':
        form = PlanillaForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.save()
            messages.success(request, f'Registro de planilla guardado para {registro.empleado}.')
            return redirect('planilla:detalle', pk=registro.pk)
    else:
        form = PlanillaForm()

    return render(request, 'planilla/form.html', {'form': form})


@login_required
def detalle_registro(request, pk):
    registro = get_object_or_404(RegistroPlanilla, pk=pk)
    resultado = calcular_planilla_completa(
        registro.sueldo_basico,
        registro.tiene_asignacion_familiar,
        registro.tipo_pension,
    )
    return render(request, 'planilla/boleta.html', {
        'empleado': registro.empleado,
        'resultado': resultado,
        'tipo_pension': registro.tipo_pension,
        'tiene_familia': registro.tiene_asignacion_familiar,
        'registro': registro,
    })


@login_required
def eliminar_registro(request, pk):
    registro = get_object_or_404(RegistroPlanilla, pk=pk)
    if request.method == 'POST':
        nombre = str(registro)
        registro.delete()
        messages.success(request, f'Registro "{nombre}" eliminado.')
        return redirect('planilla:lista')
    return render(request, 'planilla/confirmar_eliminar.html', {'registro': registro})
