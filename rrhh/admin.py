from django.contrib import admin
from .models import Empleado, Departamento


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'cedula', 'cargo', 'departamento', 'estado']
    list_filter = ['estado', 'departamento', 'tipo_contrato']
    search_fields = ['nombre', 'apellido', 'cedula', 'cargo']
    date_hierarchy = 'fecha_ingreso'
