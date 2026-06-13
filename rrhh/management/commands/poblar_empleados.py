"""
Comando para poblar la base de datos con empleados de prueba.
Uso: python manage.py poblar_empleados
"""
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from rrhh.models import Empleado, Departamento


DEPARTAMENTOS = ['Operaciones', 'Logística', 'Producción', 'Almacén', 'Administración', 'Gerencia']

NOMBRES = [
    'Carlos', 'Luis', 'Jorge', 'Miguel', 'José', 'Manuel', 'Pedro', 'Juan',
    'Roberto', 'Andrés', 'Ricardo', 'Fernando', 'Diego', 'Alejandro', 'Víctor',
    'María', 'Ana', 'Rosa', 'Carmen', 'Lucía', 'Patricia', 'Claudia', 'Silvia',
    'Mónica', 'Sandra', 'Gloria', 'Liliana', 'Verónica', 'Paola', 'Susana',
]

APELLIDOS = [
    'Quispe', 'Mamani', 'Huanca', 'Ccoa', 'Condori', 'Flores', 'García',
    'López', 'Mendoza', 'Ramirez', 'Torres', 'Vargas', 'Castro', 'Ramos',
    'Cruz', 'Rojas', 'Díaz', 'Morales', 'Herrera', 'Sánchez', 'Gutiérrez',
    'Paredes', 'Llanos', 'Huamán', 'Chávez', 'Vega', 'Salinas', 'Aguilar',
    'Castillo', 'Ríos',
]

CARGOS_OPERARIOS = [
    'Operario de Producción', 'Técnico de Mantenimiento', 'Almacenero',
    'Auxiliar de Logística', 'Operador de Máquinas', 'Ayudante de Almacén',
    'Técnico de Control de Calidad', 'Conductor', 'Estibador',
]

CARGOS_ADMIN = [
    'Asistente Administrativo', 'Asistente Contable', 'Asistente de RRHH',
    'Secretaria', 'Analista de Sistemas',
]

DIRECCIONES = [
    'Av. Arequipa 1234, Lima', 'Jr. Huallaga 456, Lima', 'Calle Los Pinos 78, Miraflores',
    'Av. Universitaria 890, San Miguel', 'Jr. Lampa 321, Centro de Lima',
    'Av. Tupac Amaru 567, Comas', 'Calle Las Flores 12, San Borja',
    'Av. Panamericana Sur 3456, Villa El Salvador', 'Jr. Cusco 890, Breña',
    'Av. Brasil 2345, Jesús María',
]


def fecha_aleatoria(inicio_año, fin_año):
    inicio = date(inicio_año, 1, 1)
    fin = date(fin_año, 12, 31)
    delta = (fin - inicio).days
    return inicio + timedelta(days=random.randint(0, delta))


class Command(BaseCommand):
    help = 'Pobla la base de datos con 30 empleados de prueba'

    def handle(self, *args, **options):
        self.stdout.write('Creando departamentos...')
        departamentos = {}
        for nombre in DEPARTAMENTOS:
            dep, _ = Departamento.objects.get_or_create(nombre=nombre)
            departamentos[nombre] = dep

        if Empleado.objects.exists():
            self.stdout.write(self.style.WARNING('Ya existen empleados. Limpiando...'))
            Empleado.objects.all().delete()

        self.stdout.write('Creando empleados...')
        creados = 0
        nombres_usados = set()

        def nombre_unico():
            for _ in range(100):
                n = random.choice(NOMBRES)
                a1 = random.choice(APELLIDOS)
                a2 = random.choice(APELLIDOS)
                clave = f"{n}{a1}{a2}"
                if clave not in nombres_usados:
                    nombres_usados.add(clave)
                    return n, a1, a2
            return NOMBRES[creados % len(NOMBRES)], APELLIDOS[creados], APELLIDOS[(creados + 1) % len(APELLIDOS)]

        # 1 Gerente General
        n, a1, a2 = nombre_unico()
        Empleado.objects.create(
            nombre=n, apellido=f"{a1} {a2}",
            cedula=f"10{creados+1:07d}",
            fecha_nacimiento=fecha_aleatoria(1970, 1980),
            genero=random.choice(['M', 'F']),
            direccion=random.choice(DIRECCIONES),
            cargo='Gerente General',
            departamento=departamentos['Gerencia'],
            fecha_ingreso=fecha_aleatoria(2018, 2020),
            tipo_contrato='indefinido',
            salario='2000.00',
            estado='activo',
        )
        creados += 1
        self.stdout.write(f'  ✔ Gerente General: {n} {a1} {a2} — S/ 2,000')

        # 5 Administrativos
        dep_admin = departamentos['Administración']
        for i, cargo in enumerate(CARGOS_ADMIN):
            n, a1, a2 = nombre_unico()
            Empleado.objects.create(
                nombre=n, apellido=f"{a1} {a2}",
                cedula=f"20{creados+1:07d}",
                fecha_nacimiento=fecha_aleatoria(1985, 1995),
                genero=random.choice(['M', 'F']),
                direccion=random.choice(DIRECCIONES),
                cargo=cargo,
                departamento=dep_admin,
                fecha_ingreso=fecha_aleatoria(2020, 2023),
                tipo_contrato=random.choice(['indefinido', 'plazo_fijo']),
                salario='1700.00',
                estado='activo',
            )
            creados += 1
            self.stdout.write(f'  ✔ {cargo}: {n} {a1} {a2} — S/ 1,700')

        # 24 Operarios en distintos departamentos
        deps_operarios = ['Operaciones', 'Logística', 'Producción', 'Almacén']
        for i in range(24):
            n, a1, a2 = nombre_unico()
            dep_nombre = deps_operarios[i % len(deps_operarios)]
            cargo = CARGOS_OPERARIOS[i % len(CARGOS_OPERARIOS)]
            Empleado.objects.create(
                nombre=n, apellido=f"{a1} {a2}",
                cedula=f"30{creados+1:07d}",
                fecha_nacimiento=fecha_aleatoria(1988, 2000),
                genero=random.choice(['M', 'F']),
                direccion=random.choice(DIRECCIONES),
                cargo=cargo,
                departamento=departamentos[dep_nombre],
                fecha_ingreso=fecha_aleatoria(2021, 2025),
                tipo_contrato=random.choice(['indefinido', 'plazo_fijo', 'honorarios']),
                salario='1250.00',
                estado=random.choice(['activo', 'activo', 'activo', 'inactivo']),
            )
            creados += 1

        self.stdout.write('  ✔ 24 operarios creados — S/ 1,250')

        total = Empleado.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ {total} empleados creados exitosamente.\n'
            f'   - 1  Gerente General     S/ 2,000\n'
            f'   - 5  Administrativos     S/ 1,700\n'
            f'   - 24 Operarios           S/ 1,250\n'
        ))
