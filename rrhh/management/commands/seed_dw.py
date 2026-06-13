"""
Comando de seed para Data Warehouse / Data Lake.
Genera 12 departamentos, 1900 empleados y registros de planilla
desde enero 2023 hasta junio 2026.

Uso:
    python manage.py seed_dw
    python manage.py seed_dw --flush     # limpia todo antes de poblar
"""
import random
from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from rrhh.models import Departamento, Empleado
from planilla.models import RegistroPlanilla

# ──────────────────────────────────────────────────────────────────────────────
# Datos maestros
# ──────────────────────────────────────────────────────────────────────────────

DEPARTAMENTOS = [
    'Gerencia', 'Administración', 'Recursos Humanos', 'Contabilidad',
    'Finanzas', 'Producción', 'Almacén', 'Logística',
    'Operaciones', 'Tecnología', 'Ventas', 'Marketing',
]

CARGOS = {
    'Gerencia':          [('Gerente General', 5500, 8000), ('Subgerente', 4000, 5500),
                          ('Asistente de Gerencia', 2200, 3200)],
    'Administración':    [('Jefe Administrativo', 2800, 3800), ('Asistente Administrativo', 1500, 2200),
                          ('Secretaria', 1400, 1900), ('Recepcionista', 1100, 1500)],
    'Recursos Humanos':  [('Jefe de RRHH', 3000, 4200), ('Analista de RRHH', 1800, 2600),
                          ('Asistente de RRHH', 1300, 1900), ('Reclutador', 1600, 2400)],
    'Contabilidad':      [('Contador General', 3200, 4500), ('Analista Contable', 2000, 3000),
                          ('Asistente Contable', 1400, 2100), ('Auxiliar Contable', 1100, 1500)],
    'Finanzas':          [('Jefe de Finanzas', 3500, 5000), ('Analista Financiero', 2200, 3200),
                          ('Tesorero', 2800, 3800), ('Asistente Financiero', 1500, 2200)],
    'Producción':        [('Jefe de Producción', 3000, 4200), ('Supervisor de Producción', 2000, 2900),
                          ('Técnico de Producción', 1400, 2000), ('Operario', 1000, 1400)],
    'Almacén':           [('Jefe de Almacén', 2600, 3600), ('Supervisor de Almacén', 1800, 2600),
                          ('Almacenero', 1100, 1600), ('Auxiliar de Almacén', 950, 1200)],
    'Logística':         [('Jefe de Logística', 3000, 4000), ('Coordinador Logístico', 2000, 3000),
                          ('Asistente de Logística', 1400, 2000), ('Conductor', 1100, 1600)],
    'Operaciones':       [('Jefe de Operaciones', 3200, 4500), ('Coordinador de Operaciones', 2200, 3200),
                          ('Analista de Operaciones', 1800, 2600), ('Asistente de Operaciones', 1300, 1900)],
    'Tecnología':        [('Jefe de TI', 4000, 6000), ('Desarrollador Senior', 3500, 5500),
                          ('Desarrollador Junior', 2000, 3500), ('Analista de Sistemas', 2500, 3800),
                          ('Soporte Técnico', 1400, 2200), ('DBA', 3000, 4500)],
    'Ventas':            [('Jefe de Ventas', 3000, 4500), ('Ejecutivo de Ventas', 1500, 2800),
                          ('Vendedor', 1100, 1800), ('Supervisor de Ventas', 2200, 3200)],
    'Marketing':         [('Jefe de Marketing', 3200, 4800), ('Analista de Marketing', 2000, 3000),
                          ('Diseñador Gráfico', 1800, 2800), ('Community Manager', 1500, 2400)],
}

NOMBRES_M = [
    'Carlos', 'Juan', 'Luis', 'Miguel', 'José', 'Pedro', 'Andrés', 'Roberto',
    'Diego', 'Manuel', 'Fernando', 'Ricardo', 'Eduardo', 'Alejandro', 'Pablo',
    'Sergio', 'Javier', 'Raúl', 'Hugo', 'Oscar', 'Gustavo', 'Alfredo', 'Ernesto',
    'Marco', 'Álvaro', 'Rodolfo', 'Víctor', 'Jorge', 'Héctor', 'César', 'Iván',
    'David', 'Rubén', 'Elías', 'Augusto', 'Martín', 'Rolando', 'Walter', 'Elvis',
    'Jhon', 'Kevin', 'Bryan', 'Christian', 'Samuel', 'Óscar', 'Daniel', 'Alex',
    'Lenin', 'Wilmer', 'Deyvis',
]

NOMBRES_F = [
    'María', 'Ana', 'Carmen', 'Rosa', 'Patricia', 'Sandra', 'Lucía', 'Jessica',
    'Karina', 'Mónica', 'Andrea', 'Claudia', 'Diana', 'Gabriela', 'Isabel',
    'Liliana', 'Milagros', 'Nadia', 'Paola', 'Rocío', 'Silvia', 'Teresa',
    'Valeria', 'Vanessa', 'Ximena', 'Yolanda', 'Nelly', 'Betty', 'Flor',
    'Melissa', 'Katia', 'Susana', 'Verónica', 'Gloria', 'Esther', 'Brenda',
    'Cindy', 'Lourdes', 'Yesenia', 'Noemi', 'Cynthia', 'Janet', 'Yaneth',
    'Ingrid', 'Lizbeth', 'Evelyn', 'Shirley', 'Fiorella', 'Mariela', 'Luz',
]

APELLIDOS = [
    'García', 'Rodríguez', 'López', 'Martínez', 'González', 'Hernández',
    'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez',
    'Díaz', 'Cruz', 'Morales', 'Reyes', 'Gutiérrez', 'Ortiz', 'Chávez',
    'Quispe', 'Mamani', 'Huanca', 'Condori', 'Apaza', 'Lazo', 'Vargas',
    'Mendoza', 'Castillo', 'Ramos', 'Espinoza', 'Rojas', 'Medina', 'Vega',
    'Salinas', 'Guerrero', 'Delgado', 'Navarro', 'Núñez', 'Prado', 'Paredes',
    'Alvarado', 'Villanueva', 'Montes', 'Herrera', 'Aguilar', 'Soto', 'Cárdenas',
    'Ccari', 'Huamán', 'Llanos', 'Tito', 'Coaquira', 'Lipa', 'Cayo', 'Ticona',
    'Huayhua', 'Puma', 'Nina', 'Catacora', 'Pilco', 'Callata', 'Masco',
]

DIRECCIONES = [
    'Av. Arequipa {n}, Lima', 'Jr. Huallaga {n}, Lima',
    'Av. Universitaria {n}, San Miguel', 'Av. Brasil {n}, Jesús María',
    'Jr. Lampa {n}, Centro', 'Av. Tupac Amaru {n}, Comas',
    'Av. Colonial {n}, Cercado', 'Jr. Cusco {n}, Breña',
    'Av. Aviación {n}, San Borja', 'Av. La Marina {n}, Pueblo Libre',
    'Calle Las Flores {n}, Miraflores', 'Av. Javier Prado {n}, La Molina',
    'Jr. Ucayali {n}, Lima', 'Av. Pachacútec {n}, Villa El Salvador',
    'Calle Bolívar {n}, Pueblo Libre', 'Av. Separadora Industrial {n}, ATE',
]

MOTIVOS_SALIDA = [
    'Renuncia voluntaria', 'Término de contrato', 'Mutuo acuerdo',
    'Despido justificado', 'Jubilación', 'Liquidación de beneficios sociales',
]

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────


def rand_date(y1: int, y2: int) -> date:
    start = date(y1, 1, 1).toordinal()
    end   = date(y2, 12, 31).toordinal()
    return date.fromordinal(random.randint(start, end))


def first_of_month(d: date) -> date:
    return d.replace(day=1)


def months_between(d1: date, d2: date) -> list[date]:
    """Lista de primeros días de mes en [d1, d2], ambos en día 1."""
    result = []
    y, m = d1.year, d1.month
    while date(y, m, 1) <= d2:
        result.append(date(y, m, 1))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return result


PERIODO_INICIO = date(2023, 1, 1)
PERIODO_FIN    = date(2026, 6, 1)


# ──────────────────────────────────────────────────────────────────────────────
# Comando
# ──────────────────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = 'Seed DW/DL: 12 departamentos, 1900 empleados, planilla 2023-2026'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Elimina todos los datos existentes antes de poblar',
        )

    def log(self, msg):
        self.stdout.write(msg)

    def ok(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def warn(self, msg):
        self.stdout.write(self.style.WARNING(msg))

    def handle(self, *args, **options):
        if options['flush']:
            self.warn('Limpiando datos existentes...')
            RegistroPlanilla.objects.all().delete()
            Empleado.objects.all().delete()
            Departamento.objects.all().delete()
            self.ok('  Tablas vaciadas.')

        # ── 1. Departamentos ──────────────────────────────────────────────────
        self.log('\n[1/3] Creando departamentos...')
        deptos = {}
        for nombre in DEPARTAMENTOS:
            obj, created = Departamento.objects.get_or_create(nombre=nombre)
            deptos[nombre] = obj
        self.ok(f'  {len(deptos)} departamentos listos.')

        # ── 2. Empleados ──────────────────────────────────────────────────────
        self.log('\n[2/3] Generando 1 900 empleados...')

        existing_count = Empleado.objects.count()
        TARGET = 1900
        to_create = max(0, TARGET - existing_count)

        if to_create == 0:
            self.warn(f'  Ya existen {existing_count} empleados — saltando.')
        else:
            # Repartición por departamento (pesos aproximados)
            DEPTO_WEIGHT = {
                'Gerencia': 10,        'Administración': 80,
                'Recursos Humanos': 60,'Contabilidad': 80,
                'Finanzas': 70,        'Producción': 260,
                'Almacén': 220,        'Logística': 200,
                'Operaciones': 220,    'Tecnología': 120,
                'Ventas': 250,         'Marketing': 130,
            }
            total_w = sum(DEPTO_WEIGHT.values())
            depto_pool: list[str] = []
            for dep, w in DEPTO_WEIGHT.items():
                depto_pool.extend([dep] * round(w / total_w * to_create))
            # Ajuste fino
            while len(depto_pool) < to_create:
                depto_pool.append(random.choice(list(DEPTO_WEIGHT.keys())))
            depto_pool = depto_pool[:to_create]
            random.shuffle(depto_pool)

            # DNI único secuencial empezando desde el máximo existente + 1
            max_dni = (
                int(Empleado.objects.order_by('-cedula').values_list('cedula', flat=True).first() or '40000000')
            )
            next_dni = max_dni + 1

            BATCH = 300
            bulk: list[Empleado] = []
            created_count = 0

            for idx, dep_nombre in enumerate(depto_pool):
                cargos_dep = CARGOS[dep_nombre]
                cargo, sal_min, sal_max = random.choice(cargos_dep)
                genero = random.choices(['M', 'F', 'O'], weights=[48, 48, 4])[0]
                nombre = random.choice(NOMBRES_M if genero == 'M' else NOMBRES_F)
                apellido = f"{random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"
                estado = random.choices(['activo', 'inactivo'], weights=[80, 20])[0]
                tipo_contrato = random.choices(
                    ['indefinido', 'plazo_fijo', 'honorarios', 'pasantia'],
                    weights=[45, 30, 18, 7]
                )[0]
                fecha_ingreso = rand_date(2015, 2025)
                fecha_nac = rand_date(1970, 2001)
                salario = Decimal(str(round(random.uniform(sal_min, sal_max), 2)))
                direccion = random.choice(DIRECCIONES).format(n=random.randint(100, 9999))
                motivo_salida = random.choice(MOTIVOS_SALIDA) if estado == 'inactivo' else ''

                bulk.append(Empleado(
                    nombre=nombre,
                    apellido=apellido,
                    cedula=str(next_dni),
                    fecha_nacimiento=fecha_nac,
                    genero=genero,
                    direccion=direccion,
                    cargo=cargo,
                    departamento=deptos[dep_nombre],
                    fecha_ingreso=fecha_ingreso,
                    tipo_contrato=tipo_contrato,
                    salario=salario,
                    estado=estado,
                    motivo_salida=motivo_salida,
                ))
                next_dni += 1
                created_count += 1

                if len(bulk) >= BATCH:
                    Empleado.objects.bulk_create(bulk)
                    bulk.clear()
                    self.log(f'  {created_count:>5} / {to_create} empleados insertados...')

            if bulk:
                Empleado.objects.bulk_create(bulk)

            total_emp = Empleado.objects.count()
            self.ok(f'  {total_emp} empleados en base de datos.')

        # ── 3. Planilla 2023-01 → 2026-06 ────────────────────────────────────
        self.log('\n[3/3] Generando registros de planilla (2023-01 → 2026-06)...')

        # Elimina planillas existentes para regenerar limpio
        existing_pl = RegistroPlanilla.objects.count()
        if existing_pl:
            self.warn(f'  Borrando {existing_pl} registros de planilla existentes...')
            RegistroPlanilla.objects.all().delete()

        empleados = list(
            Empleado.objects.select_related('departamento').all()
        )

        planilla_bulk: list[RegistroPlanilla] = []
        pl_total = 0
        BATCH_PL = 1000

        for emp_idx, emp in enumerate(empleados):
            # Determina período activo del empleado dentro de la ventana DW
            inicio_emp = max(first_of_month(emp.fecha_ingreso), PERIODO_INICIO)
            if emp.estado == 'inactivo':
                # Fecha de salida: entre 6 meses después del ingreso y 2026-05
                sal_min_date = min(
                    date(inicio_emp.year + (inicio_emp.month + 5) // 12,
                         (inicio_emp.month + 5) % 12 + 1, 1),
                    PERIODO_FIN,
                )
                fin_emp = rand_date(
                    max(sal_min_date.year, PERIODO_INICIO.year),
                    2026,
                )
                fin_emp = first_of_month(min(fin_emp, PERIODO_FIN))
            else:
                fin_emp = PERIODO_FIN

            if inicio_emp > fin_emp:
                continue

            periodos = months_between(inicio_emp, fin_emp)
            tiene_fam = random.choices([True, False], weights=[35, 65])[0]
            pension   = random.choices(['ONP', 'AFP'], weights=[55, 45])[0]

            for periodo in periodos:
                # Pequeña variación salarial mensual (±2%)
                variacion = Decimal(str(round(random.uniform(-0.02, 0.02), 4)))
                sueldo = (emp.salario * (1 + variacion)).quantize(Decimal('0.01'))

                planilla_bulk.append(RegistroPlanilla(
                    empleado=emp,
                    periodo=periodo,
                    sueldo_basico=sueldo,
                    tiene_asignacion_familiar=tiene_fam,
                    tipo_pension=pension,
                ))

            if len(planilla_bulk) >= BATCH_PL:
                RegistroPlanilla.objects.bulk_create(planilla_bulk, ignore_conflicts=True)
                pl_total += len(planilla_bulk)
                planilla_bulk.clear()
                if emp_idx % 200 == 0:
                    self.log(f'  Procesados {emp_idx + 1}/{len(empleados)} empleados '
                             f'— {pl_total:,} registros planilla...')

        if planilla_bulk:
            RegistroPlanilla.objects.bulk_create(planilla_bulk, ignore_conflicts=True)
            pl_total += len(planilla_bulk)

        # ── Resumen ───────────────────────────────────────────────────────────
        self.stdout.write('')
        self.ok('═' * 52)
        self.ok('  SEED DW/DL COMPLETADO')
        self.ok('═' * 52)
        self.ok(f'  Departamentos : {Departamento.objects.count():>8,}')
        self.ok(f'  Empleados     : {Empleado.objects.count():>8,}')
        self.ok(f'    Activos     : {Empleado.objects.filter(estado="activo").count():>8,}')
        self.ok(f'    Inactivos   : {Empleado.objects.filter(estado="inactivo").count():>8,}')
        self.ok(f'  Planilla      : {RegistroPlanilla.objects.count():>8,}')
        self.ok('  Período       :   2023-01 → 2026-06')
        self.ok('═' * 52)
