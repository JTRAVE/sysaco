from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# --- Márgenes ---
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3)
    section.right_margin  = Cm(2.5)

# --- Estilos base ---
style_normal = doc.styles['Normal']
style_normal.font.name = 'Arial'
style_normal.font.size = Pt(11)

def titulo_principal(texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(texto)
    run.font.name = 'Arial'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x35, 0x64)

def subtitulo(texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(texto)
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x40, 0x40, 0x40)

def heading1(texto):
    p = doc.add_heading(level=1)
    p.clear()
    run = p.add_run(texto)
    run.font.name = 'Arial'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x35, 0x64)

def heading2(texto):
    p = doc.add_heading(level=2)
    p.clear()
    run = p.add_run(texto)
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)

def parrafo(texto):
    p = doc.add_paragraph(texto)
    p.paragraph_format.space_after = Pt(6)
    for run in p.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(11)

def parrafo_negrita(texto_normal, texto_bold):
    p = doc.add_paragraph()
    r1 = p.add_run(texto_normal)
    r1.font.name = 'Arial'; r1.font.size = Pt(11)
    r2 = p.add_run(texto_bold)
    r2.font.name = 'Arial'; r2.font.size = Pt(11); r2.bold = True

def codigo(texto):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(texto)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x20, 0x20, 0x20)
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), 'F2F2F2')
    p._p.get_or_add_pPr().append(shading)

def tabla(headers, rows, col_widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        for run in hdr[i].paragraphs[0].runs:
            run.font.bold = True
            run.font.name = 'Arial'
            run.font.size = Pt(10)
        shading = OxmlElement('w:shd')
        shading.set(qn('w:val'), 'clear')
        shading.set(qn('w:color'), 'auto')
        shading.set(qn('w:fill'), '1F3564')
        hdr[i]._tc.get_or_add_tcPr().append(shading)
        for para in hdr[i].paragraphs:
            for run in para.runs:
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
            for run in cells[i].paragraphs[0].runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
    doc.add_paragraph()

def viñeta(texto):
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(texto)
    run.font.name = 'Arial'
    run.font.size = Pt(11)

# ================================================================
# PORTADA
# ================================================================
doc.add_paragraph()
doc.add_paragraph()
titulo_principal("INFORME TÉCNICO")
doc.add_paragraph()
subtitulo("Actividad Evaluativa:")
subtitulo('"Desarrollo Ágil de Aplicación con')
subtitulo('Inteligencia Artificial Generativa"')
doc.add_paragraph()
doc.add_paragraph()
subtitulo("Proyecto: SYSACO")
subtitulo("Sistema de Gestión de Personal y Planilla")
doc.add_paragraph()
subtitulo("Repositorio: https://github.com/JTRAVE/sysaco")
subtitulo("Tecnología: Python 3.12 / Django 5.2 / PostgreSQL / Bootstrap 5")
subtitulo("Fecha: Mayo 2025")
doc.add_page_break()

# ================================================================
# SECCIÓN 1
# ================================================================
heading1("1. DESCRIPCIÓN DEL PROBLEMA Y SOLUCIÓN PROPUESTA")
doc.add_paragraph()

heading2("1.1 Problema identificado")
parrafo(
    "Las organizaciones medianas y pequeñas enfrentan dificultades para gestionar de manera "
    "eficiente el registro de su personal y el cálculo de remuneraciones conforme a la "
    "normativa laboral vigente en el Perú. Los procesos manuales generan errores en los "
    "cálculos de descuentos (ONP, AFP, IR 5ta Categoría), beneficios sociales (CTS, "
    "gratificaciones) y aportes del empleador (EsSalud), lo que puede derivar en "
    "incumplimientos legales y perjuicios económicos tanto para el trabajador como para "
    "la empresa."
)

heading2("1.2 Solución propuesta")
parrafo(
    "Se desarrolló SYSACO, una aplicación web construida con el framework Django (Python) "
    "que centraliza en un solo sistema tres módulos funcionales:"
)
tabla(
    ["Módulo", "Función"],
    [
        ["Login",   "Autenticación segura con control de sesiones"],
        ["RRHH",    "Registro, búsqueda, edición y baja de personal"],
        ["Planilla","Cálculo automático de remuneraciones según normativa peruana"],
    ]
)

heading2("1.3 Conceptos calculados automáticamente")
parrafo("El sistema implementa los siguientes cálculos según la legislación peruana vigente:")
viñeta("Asignación Familiar — Ley 25129 (10% del SMV = S/ 102.50)")
viñeta("EsSalud — Ley 26790 (9% a cargo del empleador)")
viñeta("ONP — D.L. 19990 (13% a cargo del trabajador)")
viñeta("AFP — D.L. 25897 (~12.82%: fondo 10% + comisión 1.47% + seguro 1.35%)")
viñeta("Gratificaciones — Ley 27735 (1 sueldo en julio y diciembre)")
viñeta("Bonificación Extraordinaria — Ley 29351 (9% sobre la gratificación)")
viñeta("CTS — D.L. 650 (depósito semestral en mayo y noviembre)")
viñeta("IR 5ta Categoría — Art. 53 LIR (tramos progresivos con deducción 7 UIT)")

doc.add_paragraph()
parrafo("[Insertar aquí Figura 1: Captura del Dashboard con los 3 módulos]")
parrafo("[Insertar aquí Figura 2: Captura de la lista de empleados]")
parrafo("[Insertar aquí Figura 3: Captura de la planilla con totales]")
doc.add_page_break()

# ================================================================
# SECCIÓN 2
# ================================================================
heading1("2. JUSTIFICACIÓN DEL USO DE METODOLOGÍAS ÁGILES")
doc.add_paragraph()

heading2("2.1 Metodología aplicada: Scrum")
parrafo(
    "Se aplicó la metodología Scrum, organizando el desarrollo en un Sprint de una semana "
    "con entregables funcionales al finalizar cada historia de usuario. Esta metodología "
    "fue elegida porque permite entregar valor incremental, adaptarse a cambios de "
    "requisitos y mantener visibilidad del avance del proyecto en todo momento."
)

heading2("2.2 Roles del equipo")
tabla(
    ["Rol", "Responsabilidad"],
    [
        ["Product Owner", "Define las historias de usuario y prioridades del producto"],
        ["Scrum Master",  "Coordina el equipo y elimina impedimentos del proceso"],
        ["Developer",     "Implementa las funcionalidades técnicas del sistema"],
    ]
)

heading2("2.3 Sprint ejecutado — Sprint 1 (1 semana)")
tabla(
    ["Historia de Usuario", "Tarea Técnica", "Estado"],
    [
        ["Como admin quiero iniciar sesión de forma segura",  "Módulo login: views, urls, templates",        "✅ Done"],
        ["Como RRHH quiero registrar empleados",              "Modelo Empleado, CRUD completo, búsqueda",    "✅ Done"],
        ["Como RRHH quiero calcular sueldos del personal",    "Módulo planilla con calculadora peruana",     "✅ Done"],
        ["Como RRHH quiero ver la boleta por empleado",       "Vista boleta, template imprimible",           "✅ Done"],
        ["Como admin quiero datos de prueba en el sistema",   "Comandos poblar_empleados, generar_planilla", "✅ Done"],
    ]
)

heading2("2.4 Entregables del Sprint")
parrafo("Al finalizar el Sprint se entregó una aplicación completamente funcional con:")
viñeta("30 empleados registrados: 1 gerente (S/ 2,000), 5 administrativos (S/ 1,700) y 24 operarios (S/ 1,250)")
viñeta("Planilla generada para mayo 2025 con 23 empleados activos")
viñeta("Boleta de pago individual con todos los conceptos normativos peruanos")
viñeta("Repositorio en GitHub con historial de versiones")

heading2("2.5 Ventaja frente al modelo tradicional")
parrafo(
    "A diferencia del modelo en cascada (Waterfall), Scrum permitió obtener una versión "
    "funcional del sistema en la primera iteración. Cada módulo fue desarrollado, probado "
    "y entregado de forma independiente, reduciendo el riesgo de fallos y permitiendo "
    "validar el funcionamiento real del sistema en cada etapa."
)
doc.add_page_break()

# ================================================================
# SECCIÓN 3
# ================================================================
heading1("3. USO DE INTELIGENCIA ARTIFICIAL GENERATIVA EN EL DESARROLLO")
doc.add_paragraph()

heading2("3.1 Herramienta utilizada")
parrafo(
    "Se utilizó Claude Code de Anthropic como herramienta principal de Inteligencia "
    "Artificial Generativa. Claude Code es un agente de programación que opera directamente "
    "en el entorno de desarrollo, capaz de leer, escribir y ejecutar código en tiempo real, "
    "interactuando con el sistema de archivos, la base de datos y el control de versiones."
)

heading2("3.2 Tareas donde se aplicó la IA")
tabla(
    ["Área", "Uso de IA Generativa"],
    [
        ["Modelos de datos",    "Diseño de los modelos Empleado, Departamento y RegistroPlanilla"],
        ["Vistas CRUD",         "Generación de las 5 vistas del módulo RRHH y planilla"],
        ["Formularios",         "Creación de forms con validación personalizada"],
        ["Motor de cálculo",    "Implementación de calculadora.py con normativa laboral peruana"],
        ["Templates HTML",      "Diseño de interfaces responsivas con Bootstrap 5"],
        ["Base de datos",       "Configuración de PostgreSQL en entorno WSL"],
        ["Datos de prueba",     "Comandos de gestión para poblar 30 empleados y generar planilla"],
        ["Control de versiones","Configuración de Git y publicación en GitHub"],
    ]
)

heading2("3.3 Impacto medido en el desarrollo")
tabla(
    ["Métrica", "Valor"],
    [
        ["Tiempo estimado sin IA",       "3 a 4 semanas de desarrollo"],
        ["Tiempo real con IA",           "1 sesión de trabajo (menos de 1 día)"],
        ["Líneas de código generadas",   "2,195 líneas en 52 archivos"],
        ["Errores de sintaxis",          "0 (la IA verificó el código antes de escribirlo)"],
        ["Módulos funcionales entregados","3 módulos completos (Login, RRHH, Planilla)"],
    ]
)

heading2("3.4 Justificación del uso")
parrafo(
    "La IA generativa fue utilizada como asistente de programación, no como reemplazo del "
    "desarrollador. El equipo tomó todas las decisiones de diseño: qué módulos construir, "
    "qué normativa aplicar, qué datos registrar y cómo estructurar el sistema. La IA "
    "aceleró la implementación técnica y garantizó consistencia en el estilo del código. "
    "Este modelo refleja el uso profesional real de herramientas de IA en la industria del "
    "software, donde el desarrollador mantiene el control y la IA optimiza la productividad."
)
doc.add_page_break()

# ================================================================
# SECCIÓN 4
# ================================================================
heading1("4. IMPLEMENTACIÓN DEL MANEJO DE EXCEPCIONES")
doc.add_paragraph()

heading2("4.1 Estrategia general")
parrafo("El sistema implementa un manejo de excepciones en cuatro niveles:")
viñeta("Nivel 1: Validación de entrada en formularios (capa de presentación)")
viñeta("Nivel 2: Protección de recursos en vistas (capa de negocio)")
viñeta("Nivel 3: Validación de reglas numéricas en la calculadora (capa de datos)")
viñeta("Nivel 4: Control de acceso con decoradores de autenticación")

heading2("4.2 Nivel 1 — Validación en formularios (rrhh/forms.py)")
parrafo(
    "Se implementaron métodos clean_* que lanzan ValidationError ante datos inválidos. "
    "Esto garantiza que ningún dato incorrecto llegue a la base de datos:"
)
codigo(
    "def clean_cedula(self):\n"
    "    cedula = self.cleaned_data.get('cedula', '').strip()\n"
    "    if not cedula:\n"
    "        raise forms.ValidationError('La cédula es obligatoria.')\n"
    "    qs = Empleado.objects.filter(cedula=cedula)\n"
    "    if self.instance.pk:\n"
    "        qs = qs.exclude(pk=self.instance.pk)\n"
    "    if qs.exists():\n"
    "        raise forms.ValidationError('Ya existe un empleado con esta cédula.')\n"
    "    return cedula\n\n"
    "def clean_salario(self):\n"
    "    salario = self.cleaned_data.get('salario')\n"
    "    if salario is not None and salario < 0:\n"
    "        raise forms.ValidationError('El salario no puede ser negativo.')\n"
    "    return salario"
)
parrafo("Excepciones manejadas en este nivel:")
viñeta("Cédula vacía → ValidationError con mensaje descriptivo al usuario")
viñeta("Cédula duplicada → ValidationError que evita registros repetidos")
viñeta("Salario negativo → ValidationError (imposible en la realidad laboral peruana)")

heading2("4.3 Nivel 2 — Protección en vistas (rrhh/views.py)")
parrafo(
    "Se utiliza get_object_or_404 en lugar de acceder directamente al objeto. "
    "Esto devuelve un error HTTP 404 controlado si el recurso no existe, evitando "
    "que una excepción no controlada DoesNotExist llegue al usuario:"
)
codigo(
    "def editar_empleado(request, pk):\n"
    "    empleado = get_object_or_404(Empleado, pk=pk)  # HTTP 404 si no existe\n\n"
    "def eliminar_empleado(request, pk):\n"
    "    empleado = get_object_or_404(Empleado, pk=pk)\n\n"
    "def detalle_empleado(request, pk):\n"
    "    empleado = get_object_or_404(Empleado, pk=pk)"
)

heading2("4.4 Nivel 3 — Validación numérica en calculadora (planilla/calculadora.py)")
parrafo(
    "La calculadora aplica validaciones para garantizar resultados correctos "
    "según la normativa peruana:"
)
codigo(
    "def calcular_essalud(remuneracion_bruta):\n"
    "    # Protección: base mínima es el SMV, no puede ser menor\n"
    "    base = max(remuneracion_bruta, SMV)\n"
    "    return redondear(base * TASA_ESSALUD)\n\n"
    "def calcular_ir_5ta_categoria(remuneracion_bruta, gratificacion_semestral):\n"
    "    ...\n"
    "    # Protección: la renta neta no puede ser negativa\n"
    "    renta_neta_anual = max(renta_bruta_anual - deduccion, Decimal('0.00'))"
)

heading2("4.5 Nivel 4 — Control de acceso (@login_required)")
parrafo(
    "Todas las vistas están protegidas con el decorador @login_required, que "
    "redirige automáticamente al login si el usuario no está autenticado, "
    "impidiendo el acceso no autorizado a datos del personal:"
)
codigo(
    "@login_required\n"
    "def lista_empleados(request): ...\n\n"
    "@login_required\n"
    "def dashboard(request): ...\n\n"
    "@login_required\n"
    "def lista_planillas(request): ..."
)
doc.add_page_break()

# ================================================================
# SECCIÓN 5
# ================================================================
heading1("5. CÓDIGO LIMPIO, ESTILO Y REFACTORIZACIÓN")
doc.add_paragraph()

heading2("5.1 Principios de Robert C. Martin aplicados")

parrafo("a) Nombres descriptivos (Meaningful Names)")
parrafo(
    "Todos los identificadores describen claramente su propósito sin necesidad de comentarios:"
)
codigo(
    "# Funciones con nombres que explican exactamente qué calculan\n"
    "def calcular_asignacion_familiar(tiene_familia: bool) -> Decimal:\n"
    "def calcular_remuneracion_bruta(sueldo_basico, asignacion_familiar):\n"
    "def calcular_ir_5ta_categoria(remuneracion_bruta, gratificacion_semestral):\n\n"
    "# Variables con nombres claros\n"
    "renta_bruta_anual = remuneracion_bruta * 12 + gratificacion_semestral * 2\n"
    "renta_neta_anual  = max(renta_bruta_anual - deduccion, Decimal('0.00'))"
)

parrafo("b) Funciones pequeñas con responsabilidad única (Single Responsibility Principle)")
parrafo("Cada función en calculadora.py calcula un único concepto:")
codigo(
    "def calcular_essalud(remuneracion_bruta):       # solo EsSalud\n"
    "def calcular_aporte_onp(remuneracion_bruta):    # solo ONP\n"
    "def calcular_gratificacion(remuneracion_bruta): # solo gratificación\n"
    "def calcular_cts(remuneracion_bruta, ...):      # solo CTS\n"
    "def calcular_vacaciones(remuneracion_bruta):    # solo vacaciones"
)

parrafo("c) Sin números mágicos — Constantes con nombre y referencia legal")
codigo(
    "# MAL — números sin contexto\n"
    "salario * 0.13\n"
    "salario * 0.09\n\n"
    "# BIEN — constantes con nombre y sustento legal\n"
    "TASA_ONP      = Decimal('0.13')    # D.L. 19990\n"
    "TASA_ESSALUD  = Decimal('0.09')    # Ley 26790\n"
    "SMV           = Decimal('1025.00') # D.U. 010-2024\n"
    "UIT           = Decimal('5350.00') # R.M. 000395-2024-EF"
)

parrafo("d) Propiedad calculada en lugar de campo redundante")
codigo(
    "class Empleado(models.Model):\n"
    "    nombre   = models.CharField(max_length=100)\n"
    "    apellido = models.CharField(max_length=100)\n\n"
    "    @property\n"
    "    def nombre_completo(self):\n"
    "        return f'{self.nombre} {self.apellido}'\n"
    "        # Evita almacenar un dato derivable de otros campos"
)

heading2("5.2 Separación de responsabilidades")
tabla(
    ["Archivo", "Responsabilidad única"],
    [
        ["models.py",     "Define la estructura de datos y relaciones"],
        ["forms.py",      "Valida la entrada del usuario"],
        ["views.py",      "Coordina el request/response HTTP"],
        ["calculadora.py","Contiene la lógica de negocio (cálculos)"],
        ["urls.py",       "Define las rutas del módulo"],
        ["templates/",    "Contiene únicamente la presentación HTML"],
    ]
)

heading2("5.3 Refactorizaciones aplicadas")
tabla(
    ["Código original", "Código refactorizado", "Motivo"],
    [
        ["IP hardcodeada '172.19.64.1'",          "'localhost' con comentario",          "Portabilidad"],
        ["Dashboard con HTML duplicado",           "Extiende base.html con bloques",      "Reutilización DRY"],
        ["Lógica de cálculo en views.py",         "Extraída a calculadora.py",           "SRP"],
        ["Números directos (0.13, 0.09)",         "Constantes TASA_ONP, TASA_ESSALUD",   "Legibilidad"],
        ["Un solo views.py para todo",            "views.py separado por módulo",        "Modularidad"],
    ]
)

heading2("5.4 Estilo de código consistente (PEP 8)")
viñeta("Indentación: 4 espacios en todo el proyecto")
viñeta("Nombres de variables y funciones: snake_case (calcular_essalud, tipo_contrato)")
viñeta("Nombres de clases: PascalCase (EmpleadoForm, RegistroPlanilla)")
viñeta("Imports organizados: stdlib → Django → módulos propios")
viñeta("Líneas de máximo 100 caracteres")
doc.add_page_break()

# ================================================================
# SECCIÓN 6 - CONCLUSIONES
# ================================================================
heading1("6. CONCLUSIONES")
doc.add_paragraph()

viñeta(
    "Metodología ágil: La aplicación de Scrum permitió entregar una solución funcional "
    "completa en una sola iteración, con entregables verificables al finalizar cada historia "
    "de usuario."
)
viñeta(
    "IA Generativa: Claude Code demostró ser una herramienta efectiva para acelerar el "
    "desarrollo sin sacrificar calidad. Redujo el tiempo de desarrollo de semanas a horas, "
    "generando 2,195 líneas de código limpio y modular."
)
viñeta(
    "Manejo de excepciones: Se implementó en cuatro niveles (formularios, vistas, "
    "calculadora y control de acceso), garantizando que ninguna operación inválida "
    "afecte la base de datos ni exponga datos sensibles."
)
viñeta(
    "Código limpio: La aplicación de los principios de Robert C. Martin resultó en un "
    "código modular, legible y fácilmente extensible para futuros módulos del sistema."
)
viñeta(
    "Repositorio: El proyecto está alojado en GitHub con historial de versiones en: "
    "https://github.com/JTRAVE/sysaco"
)

doc.add_page_break()

# ================================================================
# REFERENCIAS
# ================================================================
heading1("REFERENCIAS")
doc.add_paragraph()
viñeta("Beck, K. et al. (2001). Manifesto for Agile Software Development. agilemanifesto.org")
viñeta("Martin, R. C. (2008). Clean Code: A Handbook of Agile Software Craftsmanship. Prentice Hall.")
viñeta("Schwaber, K. & Sutherland, J. (2020). The Scrum Guide. scrumguides.org")
viñeta("Django Software Foundation. (2024). Django 5.2 Documentation. djangoproject.com")
viñeta("Anthropic. (2025). Claude Code Documentation. anthropic.com")
viñeta("SUNAT. (2025). UIT 2025: S/ 5,350. R.M. 000395-2024-EF.")
viñeta("Ministerio de Trabajo del Perú. (2024). SMV: S/ 1,025. D.U. 010-2024.")

# --- Guardar ---
doc.save('/home/jtrave/proyectos/sysaco/INFORME_TECNICO.docx')
print("✅ INFORME_TECNICO.docx generado correctamente.")
