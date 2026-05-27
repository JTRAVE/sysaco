from django.db import models


class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    CONTRATO_CHOICES = [
        ('indefinido', 'Indefinido'),
        ('plazo_fijo', 'Plazo Fijo'),
        ('honorarios', 'Honorarios'),
        ('pasantia', 'Pasantía'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    # Datos personales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    direccion = models.TextField(blank=True)

    # Datos laborales
    cargo = models.CharField(max_length=100)
    departamento = models.ForeignKey(
        Departamento, on_delete=models.PROTECT, related_name='empleados'
    )
    fecha_ingreso = models.DateField()
    tipo_contrato = models.CharField(max_length=20, choices=CONTRATO_CHOICES)
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    # Estado
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    motivo_salida = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
