from django.db import models
from rrhh.models import Empleado


class RegistroPlanilla(models.Model):
    PENSION_CHOICES = [
        ('ONP', 'ONP — Sistema Nacional de Pensiones (13%)'),
        ('AFP', 'AFP — Sistema Privado de Pensiones'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='planillas')
    periodo = models.DateField(help_text="Primer día del mes del período (ej: 2025-05-01)")
    sueldo_basico = models.DecimalField(max_digits=10, decimal_places=2)
    tiene_asignacion_familiar = models.BooleanField(default=False)
    tipo_pension = models.CharField(max_length=3, choices=PENSION_CHOICES, default='ONP')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-periodo', 'empleado__apellido']
        unique_together = ('empleado', 'periodo')
        verbose_name = 'Registro de Planilla'
        verbose_name_plural = 'Registros de Planilla'

    def __str__(self):
        return f"{self.empleado} — {self.periodo.strftime('%B %Y')}"
