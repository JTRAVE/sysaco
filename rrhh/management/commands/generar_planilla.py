"""
Comando para generar registros de planilla de ejemplo para todos los empleados activos.
Uso: python manage.py generar_planilla
"""
from datetime import date
from django.core.management.base import BaseCommand
from rrhh.models import Empleado
from planilla.models import RegistroPlanilla


PERIODO = date(2025, 5, 1)  # Mayo 2025


class Command(BaseCommand):
    help = 'Genera planilla de mayo 2025 para todos los empleados activos'

    def handle(self, *args, **options):
        RegistroPlanilla.objects.filter(periodo=PERIODO).delete()

        empleados = Empleado.objects.filter(estado='activo').select_related('departamento')
        total = empleados.count()
        self.stdout.write(f'Generando planilla para {total} empleados activos — {PERIODO.strftime("%B %Y")}\n')

        for emp in empleados:
            # Asignación familiar si el contrato es indefinido (simulación)
            tiene_familia = emp.tipo_contrato == 'indefinido'

            # Gerente y administrativos en AFP, operarios en ONP
            if emp.salario >= 1700:
                tipo_pension = 'AFP'
            else:
                tipo_pension = 'ONP'

            RegistroPlanilla.objects.create(
                empleado=emp,
                periodo=PERIODO,
                sueldo_basico=emp.salario,
                tiene_asignacion_familiar=tiene_familia,
                tipo_pension=tipo_pension,
            )
            pension_label = f"{'AFP' if tipo_pension == 'AFP' else 'ONP'}"
            familia_label = '+ Asig. Familiar' if tiene_familia else ''
            self.stdout.write(
                f'  ✔ {emp.nombre_completo:<30} S/ {emp.salario}  {pension_label}  {familia_label}'
            )

        creados = RegistroPlanilla.objects.filter(periodo=PERIODO).count()
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ {creados} registros de planilla generados para {PERIODO.strftime("%B %Y")}.'
        ))
