from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from .models import Empleado
from .forms import EmpleadoForm


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
            messages.success(request, f'Empleado "{empleado.nombre_completo}" registrado correctamente.')
            return redirect('rrhh:lista')
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
            messages.success(request, f'Empleado "{empleado.nombre_completo}" actualizado correctamente.')
            return redirect('rrhh:lista')
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, 'rrhh/form.html', {'form': form, 'titulo': f'Editar: {empleado.nombre_completo}'})


@login_required
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == 'POST':
        nombre = empleado.nombre_completo
        empleado.delete()
        messages.success(request, f'Empleado "{nombre}" eliminado correctamente.')
        return redirect('rrhh:lista')

    return render(request, 'rrhh/confirmar_eliminar.html', {'empleado': empleado})


@login_required
def detalle_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return render(request, 'rrhh/detalle.html', {'empleado': empleado})
