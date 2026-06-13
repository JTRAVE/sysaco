"""
Genera el informe DW/DL en formato Word (.docx) con formato profesional.
Uso: python generar_informe.py
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Colores corporativos
AZUL_OSCURO = RGBColor(0x0F, 0x17, 0x2A)
AZUL_MEDIO  = RGBColor(0x1E, 0x40, 0xAF)
AZUL_CLARO  = RGBColor(0x37, 0x82, 0xF6)
BLANCO      = RGBColor(0xFF, 0xFF, 0xFF)
GRIS_TEXTO  = RGBColor(0x47, 0x55, 0x69)

doc = Document()

for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.5)

def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)

def heading(text, level=1, color=None, size=None, bold=True, sb=12, sa=6):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size or (18 if level==1 else 14 if level==2 else 12))
    run.font.color.rgb = color or (AZUL_OSCURO if level==1 else AZUL_MEDIO if level==2 else AZUL_CLARO)
    p.paragraph_format.space_before = Pt(sb)
    p.paragraph_format.space_after  = Pt(sa)

def body(text, bold=False, italic=False, size=10.5, color=None, sa=4):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.bold   = bold
    run.italic = italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = color
    p.paragraph_format.space_after = Pt(sa)

def code_block(text):
    p   = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name  = 'Courier New'
    run.font.size  = Pt(8.5)
    run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    p.paragraph_format.left_indent  = Cm(0.5)
    p.paragraph_format.space_after  = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  'F1F5F9')
    p._p.get_or_add_pPr().append(shd)

def kpi_table(nombre, formula, valor, perspectiva, fuente, meta):
    t = doc.add_table(rows=6, cols=2)
    t.style = 'Table Grid'
    labels = ['Nombre del KPI', 'Fórmula de cálculo', 'Valor actual (SYSACO)',
              'Perspectiva de negocio', 'Fuente en sistema', 'Meta sugerida']
    values = [nombre, formula, valor, perspectiva, fuente, meta]
    for i, (lbl, val) in enumerate(zip(labels, values)):
        row = t.rows[i]
        set_cell_bg(row.cells[0], '1E40AF')
        r0 = row.cells[0].paragraphs[0].add_run(lbl)
        r0.bold = True; r0.font.color.rgb = BLANCO; r0.font.size = Pt(9.5)
        row.cells[1].paragraphs[0].add_run(val).font.size = Pt(9.5)
    doc.add_paragraph()

# ══ PORTADA ══════════════════════════════════════════════════
doc.add_paragraph('\n\n')
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('INFORME ACADÉMICO')
r.bold = True; r.font.size = Pt(26); r.font.color.rgb = AZUL_OSCURO

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Data Warehouse, Data Lake y Modelado Multidimensional')
r.bold = True; r.font.size = Pt(16); r.font.color.rgb = AZUL_MEDIO

doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Sistema: SYSACO — Administración y Control de Personal')
r.font.size = Pt(13); r.font.color.rgb = GRIS_TEXTO

doc.add_paragraph()
t = doc.add_table(rows=1, cols=3); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.style='Table Grid'
for val, lbl, col in [('1 900','Empleados','1E40AF'),('65 285','Registros planilla','1E40AF'),('2023–2026','Período','1E40AF')]:
    idx = [('1 900','Empleados','1E40AF'),('65 285','Registros planilla','1E40AF'),('2023–2026','Período','1E40AF')].index((val,lbl,col))
    c = t.columns[idx].cells[0]; set_cell_bg(c, col)
    p2 = c.paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p2.add_run(val+'\n'); r1.bold=True; r1.font.size=Pt(16); r1.font.color.rgb=BLANCO
    r2 = p2.add_run(lbl); r2.font.size=Pt(9); r2.font.color.rgb=RGBColor(0xBF,0xDB,0xFE)

doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Junio 2026'); r.font.size=Pt(11); r.font.color.rgb=GRIS_TEXTO

doc.add_page_break()

# ══ PARTE I ══════════════════════════════════════════════════
heading('PARTE I: PREGUNTAS DE DESARROLLO', level=1)
heading('1. Entendimiento del Negocio y KPIs', level=2)
body('Empresa: SYSACO  |  Sector: Gestión de Recursos Humanos y Nómina', bold=True)
body('SYSACO es un sistema web que gestiona el ciclo de vida del personal: registro de empleados, contratos, cálculo de planilla y beneficios sociales bajo normativa laboral peruana. Cuenta con 1 900 empleados en 12 departamentos y 65 285 registros históricos de planilla (enero 2023 – junio 2026).')
doc.add_paragraph()

heading('KPI 1 — Tasa de Retención de Personal', level=3, size=11, color=AZUL_MEDIO, sb=8)
kpi_table('Tasa de Retención de Personal',
    '(Empleados activos al cierre del período ÷ Empleados activos al inicio del período) × 100',
    '(1 500 ÷ 1 900) × 100 = 78.9 %',
    'Mide la capacidad de la organización para retener a su capital humano. Una tasa alta indica estabilidad laboral, clima organizacional saludable y bajo costo de reposición. La alta gerencia lo utiliza para evaluar las políticas de compensación y bienestar.',
    'Tabla rrhh_empleado, campo estado (activo / inactivo)',
    '≥ 85 % (estándar del sector)')

heading('KPI 2 — Costo Total de Planilla Mensual', level=3, size=11, color=AZUL_MEDIO, sb=8)
kpi_table('Costo Total de Planilla Mensual',
    'Σ (sueldo_básico + asignación_familiar) de todos los empleados activos del período',
    'S/ 3 868 667.46 — junio 2026 (1 573 registros activos)',
    'Mide el gasto total en remuneraciones por período y por departamento. Permite a gerencia financiera controlar el presupuesto de personal, detectar desviaciones frente al presupuesto anual y comparar eficiencia entre áreas.',
    'Tabla planilla_registroplanilla, campos sueldo_basico y tiene_asignacion_familiar',
    'Variación ≤ ±3 % respecto al mes anterior')

heading('KPI 3 — Índice de Rotación de Personal (Turnover)', level=3, size=11, color=AZUL_MEDIO, sb=8)
kpi_table('Índice de Rotación de Personal',
    '(N.° empleados con cese en el período ÷ ((Empleados inicio + Empleados fin) ÷ 2)) × 100',
    '(400 ÷ 1 900) × 100 = 21.1 %  ⚠ Supera el estándar recomendado',
    'Mide la proporción de empleados que abandonaron la organización. Un índice elevado implica altos costos de reclutamiento, capacitación y pérdida de conocimiento institucional. Es crítico para revisar contratos, condiciones salariales y cultura organizacional.',
    'Tabla rrhh_empleado, campos estado = "inactivo" y motivo_salida',
    '≤ 10 % anual')

doc.add_paragraph()
heading('Top 5 departamentos por costo de planilla', level=3, size=10, color=GRIS_TEXTO, sb=4)
t = doc.add_table(rows=6, cols=3); t.style='Table Grid'
for j, h in enumerate(['Departamento','Empleados Activos','Costo Planilla (S/)']):
    set_cell_bg(t.rows[0].cells[j],'0F172A')
    r = t.rows[0].cells[j].paragraphs[0].add_run(h)
    r.bold=True; r.font.color.rgb=BLANCO; r.font.size=Pt(9.5)
for i,(dep,emp,costo) in enumerate([('Ventas','222','557 856.62'),('Operaciones','198','503 908.38'),
    ('Producción','222','495 552.89'),('Logística','179','418 279.26'),('Tecnología','100','366 740.79')]):
    bg='F8FAFC' if i%2==0 else 'FFFFFF'
    row=t.rows[i+1]
    for j,val in enumerate([dep,emp,costo]):
        set_cell_bg(row.cells[j],bg); row.cells[j].paragraphs[0].add_run(val).font.size=Pt(9.5)

doc.add_page_break()

# ══ TABLA COMPARATIVA ════════════════════════════════════════
heading('2. Cuadro Comparativo: Data Warehouse vs. Data Lake', level=2)

heading('Diagrama de Arquitectura — Data Warehouse', level=3, size=10, color=GRIS_TEXTO, sb=6)
for line in [
    '┌──────────────────────────────────────────────────────────────────┐',
    '│              ARQUITECTURA  DATA  WAREHOUSE                        │',
    '│  ┌──────────┐  ┌──────────┐  ┌────────────────┐  ┌───────────┐ │',
    '│  │  FUENTES │  │   ETL    │  │  DATA WAREHOUSE │  │  CONSUMO  │ │',
    '│  │  OLTP    │─▶│ Extract  │─▶│  Staging ──▶   │─▶│ Power BI  │ │',
    '│  │ SYSACO:  │  │ Transform│  │  Data Mart      │  │ Tableau   │ │',
    '│  │ empleados│  │  Load    │  │ FACT_REMUNER.   │  │ KPIs      │ │',
    '│  │ planilla │  │ Limpieza │  │ DIM_EMPLEADO    │  │ Gerencia  │ │',
    '│  │ deptos   │  │ Validac. │  │ DIM_DEPARTAMTO  │  └───────────┘ │',
    '│  └──────────┘  └──────────┘  │ DIM_TIEMPO      │               │',
    '│                               │ DIM_CONTRATO    │               │',
    '│                               └────────────────┘               │',
    '│  Esquema: Schema-on-Write  |  Datos: Estructurados               │',
    '└──────────────────────────────────────────────────────────────────┘',
]:
    code_block(line)
doc.add_paragraph()

heading('Diagrama de Arquitectura — Data Lake', level=3, size=10, color=GRIS_TEXTO, sb=6)
for line in [
    '┌──────────────────────────────────────────────────────────────────┐',
    '│                    ARQUITECTURA  DATA  LAKE                       │',
    '│  ┌──────────┐  ┌──────────────────────────────────────────────┐ │',
    '│  │  FUENTES │  │              DATA LAKE                        │ │',
    '│  │ SYSACO   │─▶│ ┌──────────┐  ┌──────────┐  ┌───────────┐  │ │',
    '│  │ (DB,JSON)│  │ │  BRONZE  │─▶│  SILVER  │─▶│   GOLD    │  │ │',
    '│  │ + Logs   │  │ │  RAW     │  │ Filtrado │  │  Curado   │  │ │',
    '│  │ + PDFs   │  │ └──────────┘  └──────────┘  └───────────┘  │ │',
    '│  └──────────┘  └──────────────────────────────────────────────┘ │',
    '│                          │                                        │',
    '│            ┌─────────────────────────────────────┐               │',
    '│            │  ML/IA  | Análisis Ad-hoc  |  OLAP  │               │',
    '│            └─────────────────────────────────────┘               │',
    '│  Esquema: Schema-on-Read   |  Datos: Cualquier formato            │',
    '└──────────────────────────────────────────────────────────────────┘',
]:
    code_block(line)
doc.add_paragraph()

heading('Tabla Comparativa', level=3, size=10, color=GRIS_TEXTO, sb=4)
criterios = [
    ('Tipo de datos soportados',
     'Solo datos ESTRUCTURADOS: tablas con esquema fijo.\nEj. SYSACO: rrhh_empleado, planilla_registroplanilla con campos numéricos y fechas definidos.',
     'Cualquier tipo: ESTRUCTURADOS (CSV), SEMIESTRUCTURADOS (JSON, XML) y NO ESTRUCTURADOS (PDFs de contratos, imágenes de DNI, correos, logs del sistema).'),
    ('Esquema\n(Schema-on-write vs. Schema-on-read)',
     'Schema-on-Write: el esquema se define y valida ANTES de cargar los datos. En SYSACO, Django Migrations define columnas antes de insertar. Si un dato no cumple el tipo es rechazado.',
     'Schema-on-Read: los datos se almacenan en bruto. El esquema se aplica AL MOMENTO DE LEERLOS con Spark o AWS Glue. Permite guardar primero y estructurar después.'),
    ('Usuarios principales y velocidad de procesamiento',
     'Usuarios: Analistas de negocio, gerentes, contadores (Power BI, Tableau).\nVelocidad: ALTA en consultas analíticas. En SYSACO: costo de planilla por departamento en milisegundos con índices pre-calculados.',
     'Usuarios: Científicos de datos, ingenieros de ML.\nVelocidad: Lento para consultas simples, superior para procesamiento masivo. Ej.: analizar 65 285 registros para predecir rotación con IA.'),
    ('Orientación\n(OLAP vs. Análisis predictivo)',
     'OLAP: responde preguntas históricas estructuradas.\n"¿Cuánto costó la planilla de Producción en Q1 2025?"\nRespuestas deterministas y rápidas.',
     'Análisis predictivo / exploratorio: descubre patrones ocultos.\n"¿Qué empleados tienen mayor probabilidad de renunciar en 3 meses?"\nCombina datos SYSACO + variables externas.'),
    ('Costo de almacenamiento',
     'Alto: requiere servidores potentes (SQL Server, Redshift, Snowflake). El diseño limpio implica ETL costoso en tiempo y recursos.',
     'Bajo: almacenamiento en objetos (S3, Azure Data Lake, HDFS). Guardar los 65 285 registros de SYSACO cuesta fracciones de centavo en la nube.'),
    ('Calidad del dato',
     'Alta: cada registro pasa por transformaciones y validaciones. En SYSACO, Django ORM valida cada RegistroPlanilla antes de persistirlo.',
     'Variable: los datos entran sin filtro (Bronze). La calidad se garantiza en capas Silver y Gold. Puede contener duplicados en la capa Raw.'),
    ('Caso de uso en SYSACO',
     'Dashboard de Capital Humano: KPIs de retención, costo de planilla por departamento, distribución por contrato. Datos 2023-2026 para consultas OLAP inmediatas.',
     'Almacenar logs de acceso, contratos en PDF, historial salarial en JSON crudo, para construir modelos predictivos de rotación o detección de anomalías en planilla.'),
]
t = doc.add_table(rows=len(criterios)+1, cols=3); t.style='Table Grid'
for j,h in enumerate(['Criterio de Comparación','Data Warehouse (DW)','Data Lake (DL)']):
    set_cell_bg(t.rows[0].cells[j],'0F172A')
    r=t.rows[0].cells[j].paragraphs[0].add_run(h)
    r.bold=True; r.font.color.rgb=BLANCO; r.font.size=Pt(9.5)
    t.rows[0].cells[j].paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
for i,(crit,dw,dl) in enumerate(criterios):
    bg='EFF6FF' if i%2==0 else 'FFFFFF'
    row=t.rows[i+1]
    set_cell_bg(row.cells[0],'DBEAFE')
    rc=row.cells[0].paragraphs[0].add_run(crit); rc.bold=True; rc.font.size=Pt(9); rc.font.color.rgb=AZUL_OSCURO
    for j,val in enumerate([dw,dl]):
        set_cell_bg(row.cells[j+1],bg); row.cells[j+1].paragraphs[0].add_run(val).font.size=Pt(9)

doc.add_page_break()

# ══ PARTE II ═════════════════════════════════════════════════
heading('PARTE II: ACTIVIDAD PRÁCTICA — Modelado Estrella', level=1)
body('Nota: SYSACO gestiona Recursos Humanos y Planilla. Se aplica la misma metodología de Modelo Estrella adaptando el proceso de negocio a Gestión de Remuneraciones, equivalente al proceso de Ventas en una empresa comercial.', italic=True, color=GRIS_TEXTO)
doc.add_paragraph()

heading('Tablas OLTP de Origen (Input)', level=2)
for line in [
    'rrhh_departamento          rrhh_empleado',
    '─────────────────          ──────────────────────────────',
    'id           (PK)          id               (PK)',
    'nombre                     nombre / apellido',
    '                           cedula           (UNIQUE)',
    '                           cargo',
    '                           departamento_id  (FK)',
    '                           fecha_ingreso',
    '                           tipo_contrato',
    '                           salario / estado',
    '',
    'planilla_registroplanilla',
    '──────────────────────────',
    'id                   (PK)',
    'empleado_id          (FK → empleado)',
    'periodo              (DATE — primer día del mes)',
    'sueldo_basico',
    'tiene_asignacion_familiar',
    'tipo_pension',
]:
    code_block(line)
doc.add_paragraph()

heading('Diseño del Modelo Estrella', level=2)
t = doc.add_table(rows=6, cols=3); t.style='Table Grid'
for j,h in enumerate(['Componente','Tabla','Justificación']):
    set_cell_bg(t.rows[0].cells[j],'0F172A')
    r=t.rows[0].cells[j].paragraphs[0].add_run(h)
    r.bold=True; r.font.color.rgb=BLANCO; r.font.size=Pt(9.5)
rows2=[('Tabla de Hechos','FACT_REMUNERACION','Cada registro es un pago mensual; contiene métricas: sueldo, descuentos, neto'),
       ('Dimensión 1','DIM_EMPLEADO','Quién recibe la remuneración (≡ Cliente en Ventas)'),
       ('Dimensión 2','DIM_DEPARTAMENTO','Dónde trabaja (≡ Región/Ciudad en Ventas)'),
       ('Dimensión 3','DIM_TIEMPO','Cuándo se realizó el pago: mes, trimestre, año'),
       ('Dimensión 4','DIM_CONTRATO','Modalidad laboral (≡ Categoría de Producto en Ventas)')]
for i,(comp,tabla,just) in enumerate(rows2):
    bg='EFF6FF' if i%2==0 else 'FFFFFF'
    row=t.rows[i+1]; set_cell_bg(row.cells[0],'DBEAFE')
    r=row.cells[0].paragraphs[0].add_run(comp); r.bold=True; r.font.size=Pt(9.5)
    for j,val in enumerate([tabla,just]):
        set_cell_bg(row.cells[j+1],bg); row.cells[j+1].paragraphs[0].add_run(val).font.size=Pt(9.5)
doc.add_paragraph()

heading('Diagrama ERD — Modelo Estrella', level=3, size=11, color=GRIS_TEXTO)
for line in [
    '                    ┌─────────────────────────┐',
    '                    │       DIM_TIEMPO         │',
    '                    │ id_tiempo      PK        │',
    '                    │ periodo                  │',
    '                    │ mes / nombre_mes         │',
    '                    │ trimestre / semestre     │',
    '                    │ anio                     │',
    '                    └────────────┬─────────────┘',
    '                                 │ FK',
    ' ┌──────────────────┐            │         ┌──────────────────────┐',
    ' │   DIM_EMPLEADO   │            │         │  DIM_DEPARTAMENTO    │',
    ' │ id_empleado  PK  │            │         │ id_departamento  PK  │',
    ' │ nombre_completo  ├────FK──────┤──FK─────┤ nombre_departamento  │',
    ' │ cargo / genero   │    ┌───────┴──────────────────────┐         │',
    ' │ estado           │    │    FACT_REMUNERACION          │         │',
    ' └──────────────────┘ FK │ id_registro         PK       │         │',
    '         └─────────────▶ │ id_tiempo    FK              │         │',
    '                         │ id_empleado  FK              │         │',
    '                         │ id_departamento  FK          │   FK    │',
    '                         │ id_contrato  FK              │─────────┘',
    '                         │ sueldo_basico  [métrica]     │',
    '                         │ asignacion_familiar [métrica]│',
    '                         │ descuento_pension  [métrica] │',
    '                         │ sueldo_bruto  [métrica]      │',
    '                         │ sueldo_neto   [métrica]      │',
    '                         └──────────────────────────────┘',
    '                                      │ FK',
    '                    ┌─────────────────┴────────────────┐',
    '                    │         DIM_CONTRATO              │',
    '                    │ id_contrato       PK              │',
    '                    │ tipo_contrato                     │',
    '                    │ descripcion                       │',
    '                    │ sistema_pension                   │',
    '                    └───────────────────────────────────┘',
]:
    code_block(line)

doc.add_page_break()

heading('Código SQL — Creación de Tablas e Inserción de Datos', level=2)
sql_lines = """-- ═══════════════════════════════════════════════════════════
--  MODELO ESTRELLA SYSACO: Gestión de Remuneraciones
-- ═══════════════════════════════════════════════════════════

-- ── DIMENSIÓN: TIEMPO ──────────────────────────────────────
CREATE TABLE DIM_TIEMPO (
    id_tiempo   SERIAL       PRIMARY KEY,
    periodo     DATE         NOT NULL,
    mes         SMALLINT     NOT NULL,
    nombre_mes  VARCHAR(20)  NOT NULL,
    trimestre   SMALLINT     NOT NULL,
    semestre    SMALLINT     NOT NULL,
    anio        SMALLINT     NOT NULL
);
INSERT INTO DIM_TIEMPO (periodo,mes,nombre_mes,trimestre,semestre,anio) VALUES
    ('2025-01-01', 1,'Enero',   1,1,2025),
    ('2025-04-01', 4,'Abril',   2,1,2025),
    ('2025-07-01', 7,'Julio',   3,2,2025),
    ('2025-10-01',10,'Octubre', 4,2,2025),
    ('2026-01-01', 1,'Enero',   1,1,2026),
    ('2026-04-01', 4,'Abril',   2,1,2026),
    ('2026-06-01', 6,'Junio',   2,1,2026);

-- ── DIMENSIÓN: DEPARTAMENTO ────────────────────────────────
CREATE TABLE DIM_DEPARTAMENTO (
    id_departamento     SERIAL      PRIMARY KEY,
    nombre_departamento VARCHAR(80) NOT NULL,
    area_negocio        VARCHAR(40) NOT NULL
);
INSERT INTO DIM_DEPARTAMENTO (nombre_departamento,area_negocio) VALUES
    ('Gerencia','Dirección'),('Administración','Soporte'),
    ('Recursos Humanos','Soporte'),('Contabilidad','Finanzas'),
    ('Finanzas','Finanzas'),('Producción','Operaciones'),
    ('Almacén','Operaciones'),('Logística','Operaciones'),
    ('Operaciones','Operaciones'),('Tecnología','Soporte'),
    ('Ventas','Comercial'),('Marketing','Comercial');

-- ── DIMENSIÓN: EMPLEADO ────────────────────────────────────
CREATE TABLE DIM_EMPLEADO (
    id_empleado     SERIAL       PRIMARY KEY,
    nombre_completo VARCHAR(200) NOT NULL,
    cargo           VARCHAR(100) NOT NULL,
    genero          CHAR(1)      NOT NULL,
    estado          VARCHAR(10)  NOT NULL
);
INSERT INTO DIM_EMPLEADO (nombre_completo,cargo,genero,estado) VALUES
    ('José García Torres',   'Gerente General',       'M','activo'),
    ('María López Quispe',   'Jefa de Finanzas',      'F','activo'),
    ('Carlos Mamani Flores', 'Desarrollador Senior',  'M','activo'),
    ('Patricia Condori Vega','Analista Contable',     'F','activo'),
    ('Diego Torres Huanca',  'Ejecutivo de Ventas',   'M','activo'),
    ('Rosa Vargas Chávez',   'Analista de RRHH',      'F','activo'),
    ('Marco Salinas Ramos',  'Jefe de Producción',    'M','activo'),
    ('Sandra Herrera Díaz',  'Coord. Logística',      'F','inactivo'),
    ('Víctor Espinoza Cruz', 'Operario',              'M','inactivo'),
    ('Lucía Mendoza Rojas',  'Community Manager',     'F','activo');

-- ── DIMENSIÓN: CONTRATO ────────────────────────────────────
CREATE TABLE DIM_CONTRATO (
    id_contrato     SERIAL       PRIMARY KEY,
    tipo_contrato   VARCHAR(30)  NOT NULL,
    descripcion     VARCHAR(150) NOT NULL,
    sistema_pension VARCHAR(3)   NOT NULL
);
INSERT INTO DIM_CONTRATO (tipo_contrato,descripcion,sistema_pension) VALUES
    ('indefinido','Contrato indefinido, plena estabilidad laboral','ONP'),
    ('indefinido','Contrato indefinido, plena estabilidad laboral','AFP'),
    ('plazo_fijo','Contrato sujeto a modalidad, duración determinada','ONP'),
    ('honorarios','Locación de servicios, sin relación de dependencia','AFP'),
    ('pasantia',  'Prácticas preprofesionales, sueldo reducido','ONP');

-- ── TABLA DE HECHOS ────────────────────────────────────────
CREATE TABLE FACT_REMUNERACION (
    id_registro         SERIAL        PRIMARY KEY,
    id_tiempo           INT           NOT NULL REFERENCES DIM_TIEMPO(id_tiempo),
    id_empleado         INT           NOT NULL REFERENCES DIM_EMPLEADO(id_empleado),
    id_departamento     INT           NOT NULL REFERENCES DIM_DEPARTAMENTO(id_departamento),
    id_contrato         INT           NOT NULL REFERENCES DIM_CONTRATO(id_contrato),
    sueldo_basico       NUMERIC(10,2) NOT NULL,
    asignacion_familiar NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    descuento_pension   NUMERIC(10,2) NOT NULL,
    sueldo_bruto        NUMERIC(10,2) NOT NULL,
    sueldo_neto         NUMERIC(10,2) NOT NULL
);
-- Cálculos: bruto = básico + AF | ONP = bruto×0.13 | AFP = bruto×0.10
INSERT INTO FACT_REMUNERACION
  (id_tiempo,id_empleado,id_departamento,id_contrato,
   sueldo_basico,asignacion_familiar,descuento_pension,sueldo_bruto,sueldo_neto)
VALUES
  (1,1, 1,1,6500.00,102.50, 862.33,6602.50,5740.18),
  (1,2, 5,2,4200.00,102.50, 430.25,4302.50,3872.25),
  (1,3,10,2,3800.00,  0.00, 380.00,3800.00,3420.00),
  (1,4, 4,3,2100.00,102.50, 286.33,2202.50,1916.18),
  (1,5,11,3,1650.00,  0.00, 214.50,1650.00,1435.50),
  (2,1, 1,1,6500.00,102.50, 862.33,6602.50,5740.18),
  (2,6, 3,1,1900.00,102.50, 260.33,2002.50,1742.18),
  (2,7, 6,3,3200.00,  0.00, 416.00,3200.00,2784.00),
  (3,3,10,2,3850.00,  0.00, 385.00,3850.00,3465.00),
  (5,5,11,3,1720.00,102.50, 237.33,1822.50,1585.18);""".split('\n')

for line in sql_lines:
    code_block(line)
doc.add_paragraph()

heading('Consulta OLAP — Explotación de Datos', level=2)
body('Consulta analítica que consolida remuneraciones totales agrupadas por Departamento y Tipo de Contrato durante el año 2025 (equivalente a "ventas por Categoría de Producto y Ciudad del Cliente"):')
doc.add_paragraph()

olap_lines = """-- ═══════════════════════════════════════════════════════════
-- OLAP: Consolidado por Departamento y Tipo de Contrato 2025
-- ═══════════════════════════════════════════════════════════
SELECT
    d.nombre_departamento      AS departamento,
    d.area_negocio             AS area,
    c.tipo_contrato            AS modalidad_contrato,
    t.trimestre,  t.anio,
    COUNT(f.id_registro)       AS total_pagos,
    SUM(f.sueldo_basico)       AS total_sueldo_basico,
    SUM(f.sueldo_bruto)        AS total_bruto,
    SUM(f.sueldo_neto)         AS total_neto,
    AVG(f.sueldo_neto)         AS promedio_neto,
    MAX(f.sueldo_neto)         AS sueldo_max,
    MIN(f.sueldo_neto)         AS sueldo_min
FROM  FACT_REMUNERACION   f
JOIN  DIM_TIEMPO           t ON f.id_tiempo       = t.id_tiempo
JOIN  DIM_EMPLEADO         e ON f.id_empleado     = e.id_empleado
JOIN  DIM_DEPARTAMENTO     d ON f.id_departamento = d.id_departamento
JOIN  DIM_CONTRATO         c ON f.id_contrato     = c.id_contrato
WHERE t.anio = 2025
  AND e.estado = 'activo'
GROUP BY ROLLUP(d.area_negocio, d.nombre_departamento, c.tipo_contrato, t.trimestre)
ORDER BY d.area_negocio, d.nombre_departamento, t.trimestre;

-- ── Comparativo interanual 2024 vs 2025 ─────────────────────
SELECT
    d.nombre_departamento,
    SUM(CASE WHEN t.anio=2024 THEN f.sueldo_neto ELSE 0 END) AS total_2024,
    SUM(CASE WHEN t.anio=2025 THEN f.sueldo_neto ELSE 0 END) AS total_2025,
    ROUND(
      (SUM(CASE WHEN t.anio=2025 THEN f.sueldo_neto ELSE 0 END) -
       SUM(CASE WHEN t.anio=2024 THEN f.sueldo_neto ELSE 0 END))
      / NULLIF(SUM(CASE WHEN t.anio=2024 THEN f.sueldo_neto ELSE 0 END),0)*100
    ,2) AS variacion_pct
FROM FACT_REMUNERACION f
JOIN DIM_TIEMPO       t ON f.id_tiempo=t.id_tiempo
JOIN DIM_DEPARTAMENTO d ON f.id_departamento=d.id_departamento
WHERE t.anio IN (2024,2025)
GROUP BY d.nombre_departamento
ORDER BY total_2025 DESC;""".split('\n')

for line in olap_lines:
    code_block(line)

doc.add_page_break()

# ══ CONCLUSIONES ════════════════════════════════════════════
heading('Conclusiones', level=2)
conclusiones = [
    ('DW vs DL en SYSACO: ',
     'El sistema opera actualmente como OLTP. Para construir el Data Warehouse se aplica ETL hacia el modelo estrella diseñado. El Data Lake es útil para almacenar contratos PDF, logs y datos de mercado laboral destinados a modelos predictivos de rotación.'),
    ('Alerta en KPI de Rotación: ',
     'La Tasa de Retención (78.9%) está por debajo del estándar recomendado de ≥ 85%. El Índice de Rotación (21.1%) con 400 empleados inactivos supera el límite de 10% anual. Se recomienda revisar motivos de salida y políticas de compensación por departamento.'),
    ('Valor del Modelo Estrella: ',
     'El modelo diseñado permite responder preguntas OLAP como "¿cuánto se invirtió en planilla en Producción en Q3 2025?" en milisegundos, imposible con consultas directas sobre la base OLTP con 65 285 registros históricos. GROUP BY ROLLUP genera subtotales automáticos por jerarquía.'),
]
for titulo, texto in conclusiones:
    p = doc.add_paragraph()
    r1 = p.add_run(titulo); r1.bold=True; r1.font.size=Pt(10.5); r1.font.color.rgb=AZUL_OSCURO
    r2 = p.add_run(texto);  r2.font.size=Pt(10.5)
    p.paragraph_format.space_after = Pt(8)

doc.add_paragraph()
p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('─── Fin del Informe — SYSACO, junio 2026 ───')
r.font.size=Pt(9); r.font.color.rgb=GRIS_TEXTO; r.italic=True

out = '/home/jtrave/proyectos/sysaco/Informe_DW_DL_SYSACO.docx'
doc.save(out)
print(f'Documento generado: {out}')
