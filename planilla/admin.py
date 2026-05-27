from django.contrib import admin
from .models import RegistroPlanilla


@admin.register(RegistroPlanilla)
class RegistroPlanillaAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'periodo', 'sueldo_basico', 'tipo_pension', 'tiene_asignacion_familiar']
    list_filter = ['tipo_pension', 'periodo']
    search_fields = ['empleado__nombre', 'empleado__apellido']
    date_hierarchy = 'periodo'
