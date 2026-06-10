# INFORME TÉCNICO
## Actividad Evaluativa: "Desarrollo Ágil de Aplicación con Inteligencia Artificial Generativa"

**Proyecto:** SYSACO — Sistema de Gestión de Personal y Planilla
**Repositorio:** https://github.com/JTRAVE/sysaco
**Tecnología:** Python 3.12 / Django 5.2 / PostgreSQL / Bootstrap 5
**Fecha:** Mayo 2025

---

## 1. DESCRIPCIÓN DEL PROBLEMA Y SOLUCIÓN PROPUESTA

### 1.1 Problema identificado

Las organizaciones medianas y pequeñas enfrentan dificultades para gestionar de manera
eficiente el registro de su personal y el cálculo de remuneraciones conforme a la normativa
laboral vigente en el Perú. Los procesos manuales generan errores en los cálculos de
descuentos (ONP, AFP, IR 5ta Categoría), beneficios sociales (CTS, gratificaciones) y aportes
del empleador (EsSalud), lo que puede derivar en incumplimientos legales y perjuicios
económicos tanto para el trabajador como para la empresa.

### 1.2 Solución propuesta

Se desarrolló SYSACO, una aplicación web construida con el framework Django (Python) que
centraliza en un solo sistema tres módulos funcionales:

| Módulo     | Función                                                        |
|------------|----------------------------------------------------------------|
| Login      | Autenticación segura con control de sesiones                   |
| RRHH       | Registro, búsqueda, edición y baja de personal                 |
| Planilla   | Cálculo automático de remuneraciones según normativa peruana   |

### 1.3 Conceptos calculados automáticamente

El sistema implementa los siguientes cálculos según la legislación peruana vigente:

- Asignación Familiar — Ley 25129 (10% del SMV = S/ 102.50)
- EsSalud — Ley 26790 (9% a cargo del empleador)
- ONP — D.L. 19990 (13% a cargo del trabajador)
- AFP — D.L. 25897 (~12.82%: fondo 10% + comisión 1.47% + seguro 1.35%)
- Gratificaciones — Ley 27735 (1 sueldo en julio y diciembre)
- Bonificación Extraordinaria — Ley 29351 (9% sobre gratificación)
- CTS — D.L. 650 (depósito semestral en mayo y noviembre)
- IR 5ta Categoría — Art. 53 LIR (tramos progresivos con deducción 7 UIT)

---

## 2. JUSTIFICACIÓN DEL USO DE METODOLOGÍAS ÁGILES

### 2.1 Metodología aplicada: Scrum

Se aplicó la metodología Scrum, organizando el desarrollo en un Sprint de una semana con
entregables funcionales al finalizar cada historia de usuario. Esta metodología fue elegida
porque permite entregar valor incremental, adaptarse a cambios de requisitos y mantener
visibilidad del avance del proyecto.

### 2.2 Roles del equipo

| Rol           | Responsabilidad                                      |
|---------------|------------------------------------------------------|
| Product Owner | Define las historias de usuario y prioridades        |
| Scrum Master  | Coordina el equipo y elimina impedimentos            |
| Developer     | Implementa las funcionalidades del sistema           |

### 2.3 Sprint ejecutado

**Sprint 1 — Duración: 1 semana**

| Historia de Usuario                              | Tarea técnica                              | Estado  |
|--------------------------------------------------|--------------------------------------------|---------|
| Como admin quiero iniciar sesión de forma segura | Módulo login: views, urls, templates       | ✅ Done |
| Como RRHH quiero registrar empleados             | Modelo Empleado, CRUD completo, búsqueda   | ✅ Done |
| Como RRHH quiero calcular sueldos del personal   | Módulo planilla con calculadora peruana    | ✅ Done |
| Como RRHH quiero ver la boleta por empleado      | Vista boleta, template imprimible          | ✅ Done |
| Como admin quiero datos de prueba en el sistema  | Comandos poblar_empleados, generar_planilla| ✅ Done |

### 2.4 Entregables del Sprint

Al finalizar el Sprint se entregó una aplicación completamente funcional con:
- 30 empleados registrados (1 gerente, 5 administrativos, 24 operarios)
- Planilla generada para mayo 2025 con 23 empleados activos
- Boleta de pago individual con todos los conceptos normativos

### 2.5 Justificación frente a metodologías tradicionales

A diferencia del modelo en cascada (Waterfall), Scrum permitió obtener una versión funcional
del sistema en la primera iteración. Cada módulo fue desarrollado, probado y entregado de
forma independiente, reduciendo el riesgo de fallos y permitiendo validar el funcionamiento
real del sistema en cada etapa.

---

## 3. USO DE INTELIGENCIA ARTIFICIAL GENERATIVA EN EL DESARROLLO

### 3.1 Herramienta utilizada

Se utilizó **Claude Code de Anthropic** como herramienta principal de Inteligencia Artificial
Generativa. Claude Code es un agente de programación que opera directamente en el entorno
de desarrollo, capaz de leer, escribir y ejecutar código en tiempo real.

### 3.2 Tareas donde se aplicó la IA

| Área                  | Uso de IA                                                          |
|-----------------------|--------------------------------------------------------------------|
| Modelos de datos      | Diseño de los modelos Empleado, Departamento y RegistroPlanilla    |
| Vistas CRUD           | Generación de las 5 vistas del módulo RRHH y planilla             |
| Formularios           | Creación de forms con validación personalizada                     |
| Motor de cálculo      | Implementación de calculadora.py con normativa peruana             |
| Templates HTML        | Diseño de interfaces con Bootstrap 5                               |
| Base de datos         | Configuración de PostgreSQL en WSL                                 |
| Datos de prueba       | Comandos de gestión para poblar 30 empleados y generar planilla    |
| Control de versiones  | Configuración de Git y subida a GitHub                             |

### 3.3 Impacto medido en el desarrollo

- **Tiempo estimado sin IA:** 3 a 4 semanas de desarrollo
- **Tiempo real con IA:** 1 sesión de trabajo (menos de 1 día)
- **Líneas de código generadas:** 2,195 líneas en 52 archivos
- **Errores de sintaxis:** 0 (la IA verificó el código antes de escribirlo)

### 3.4 Justificación del uso

La IA generativa fue utilizada como asistente de programación, no como reemplazo del
desarrollador. El equipo tomó todas las decisiones de diseño (qué módulos construir, qué
normativa aplicar, qué datos registrar), mientras la IA aceleró la implementación técnica.
Este modelo de trabajo refleja el uso profesional real de herramientas de IA en la industria
del software, donde el desarrollador mantiene el control y la IA optimiza la productividad.

---

## 4. IMPLEMENTACIÓN DEL MANEJO DE EXCEPCIONES

### 4.1 Estrategia general

El sistema implementa un manejo de excepciones en tres niveles:
1. Validación de entrada en formularios (capa de presentación)
2. Protección de recursos en vistas (capa de negocio)
3. Validación de reglas de negocio en la calculadora (capa de datos)

### 4.2 Nivel 1 — Validación en formularios (rrhh/forms.py)

Se implementaron métodos `clean_*` que lanzan `ValidationError` ante datos inválidos:

```python
def clean_cedula(self):
    cedula = self.cleaned_data.get('cedula', '').strip()
    if not cedula:
        raise forms.ValidationError("La cédula es obligatoria.")
    qs = Empleado.objects.filter(cedula=cedula)
    if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)
    if qs.exists():
        raise forms.ValidationError("Ya existe un empleado con esta cédula.")
    return cedula

def clean_salario(self):
    salario = self.cleaned_data.get('salario')
    if salario is not None and salario < 0:
        raise forms.ValidationError("El salario no puede ser negativo.")
    return salario
```

**Excepciones manejadas:**
- Cédula vacía → ValidationError con mensaje descriptivo
- Cédula duplicada → ValidationError (evita registros duplicados)
- Salario negativo → ValidationError (imposible en la realidad laboral)

### 4.3 Nivel 2 — Protección en vistas (rrhh/views.py)

Se utiliza `get_object_or_404` en lugar de acceder directamente al objeto, lo que
devuelve un error HTTP 404 controlado si el recurso no existe:

```python
def editar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    ...

def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    ...

def detalle_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    ...
```

Sin este manejo, si un usuario accede a `/rrhh/999/` con un ID inexistente, el
sistema lanzaría una excepción no controlada `DoesNotExist`. Con `get_object_or_404`
el error es capturado y se muestra una respuesta HTTP apropiada.

### 4.4 Nivel 3 — Validación en calculadora (planilla/calculadora.py)

La calculadora aplica validaciones numéricas para garantizar resultados correctos:

```python
def calcular_essalud(remuneracion_bruta):
    # Evita que la base de cálculo sea menor al SMV (protección normativa)
    base = max(remuneracion_bruta, SMV)
    return redondear(base * TASA_ESSALUD)

def calcular_ir_5ta_categoria(remuneracion_bruta, gratificacion_semestral):
    ...
    # Evita renta neta negativa (si el sueldo no supera las 7 UIT de deducción)
    renta_neta_anual = max(renta_bruta_anual - deduccion, Decimal('0.00'))
    ...
```

### 4.5 Nivel 4 — Control de acceso

Todas las vistas están protegidas con el decorador `@login_required`, que redirige
automáticamente al login si el usuario no está autenticado:

```python
@login_required
def lista_empleados(request):
    ...

@login_required
def dashboard(request):
    ...
```

---

## 5. CÓDIGO LIMPIO, ESTILO Y REFACTORIZACIÓN

### 5.1 Principios de Robert C. Martin aplicados

#### a) Nombres descriptivos (Meaningful Names)

Todos los identificadores describen claramente su propósito:

```python
# Correcto — nombres que explican qué hacen
def calcular_asignacion_familiar(tiene_familia: bool) -> Decimal:
def calcular_remuneracion_bruta(sueldo_basico, asignacion_familiar):
def calcular_ir_5ta_categoria(remuneracion_bruta, gratificacion_semestral):

# Variables con nombres claros
renta_bruta_anual = remuneracion_bruta * 12 + gratificacion_semestral * 2
deduccion_7uit    = UIT * Decimal('7')
renta_neta_anual  = max(renta_bruta_anual - deduccion, Decimal('0.00'))
```

#### b) Funciones pequeñas con responsabilidad única (Single Responsibility)

Cada función en `calculadora.py` calcula un único concepto:

```python
def calcular_essalud(remuneracion_bruta):      # solo EsSalud
def calcular_aporte_onp(remuneracion_bruta):   # solo ONP
def calcular_gratificacion(remuneracion_bruta): # solo gratificación
def calcular_cts(remuneracion_bruta, ...):      # solo CTS
def calcular_vacaciones(remuneracion_bruta):    # solo vacaciones
```

La función `calcular_planilla_completa()` las orquesta sin duplicar lógica.

#### c) Separación de responsabilidades (Separation of Concerns)

El proyecto está organizado en capas bien definidas:

| Archivo              | Responsabilidad única                          |
|----------------------|------------------------------------------------|
| models.py            | Solo define la estructura de datos             |
| forms.py             | Solo valida entrada del usuario                |
| views.py             | Solo coordina request/response                 |
| calculadora.py       | Solo contiene lógica de negocio (cálculos)     |
| urls.py              | Solo define rutas                              |
| templates/           | Solo contiene presentación HTML                |

#### d) Constantes con nombre en lugar de números mágicos (No Magic Numbers)

```python
# MAL — números sin contexto
salario * 0.13
salario * 0.09

# BIEN — constantes con nombre y referencia legal
TASA_ONP     = Decimal('0.13')   # D.L. 19990
TASA_ESSALUD = Decimal('0.09')   # Ley 26790
SMV          = Decimal('1025.00') # D.U. 010-2024
UIT          = Decimal('5350.00') # R.M. 000395-2024-EF
```

#### e) Modularidad y reutilización

El modelo `Departamento` fue separado del modelo `Empleado` para evitar duplicación
y permitir reutilización:

```python
class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

class Empleado(models.Model):
    departamento = models.ForeignKey(
        Departamento, on_delete=models.PROTECT, related_name='empleados'
    )
```

#### f) Propiedad calculada en lugar de campo redundante

```python
class Empleado(models.Model):
    nombre   = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
        # Evita almacenar dato que puede derivarse de otros campos
```

### 5.2 Estilo de código consistente (PEP 8)

- Indentación: 4 espacios en todo el proyecto
- Nombres de variables y funciones: `snake_case`
- Nombres de clases: `PascalCase` (EmpleadoForm, RegistroPlanilla)
- Líneas de máximo 100 caracteres
- Imports organizados: stdlib → Django → módulos propios

### 5.3 Refactorización aplicada

Durante el desarrollo se aplicaron las siguientes refactorizaciones:

| Antes                                          | Después                                         | Motivo                        |
|------------------------------------------------|-------------------------------------------------|-------------------------------|
| Un solo archivo views.py con todo              | views.py separado por módulo (login/rrhh/planilla)| Separación de responsabilidades|
| IP hardcodeada '172.19.64.1' en settings.py   | 'localhost' con comentario explicativo          | Portabilidad del proyecto      |
| Dashboard con HTML duplicado                   | Extiende base.html con bloques                  | Reutilización de templates     |
| Lógica de cálculo en views.py                 | Extraída a calculadora.py                       | Single Responsibility Principle|
| Números directos (0.13, 0.09) en cálculos     | Constantes nombradas (TASA_ONP, TASA_ESSALUD)  | Legibilidad y mantenibilidad   |

---

## 6. CONCLUSIONES

1. **Metodología ágil:** La aplicación de Scrum permitió entregar una solución funcional
   completa en una sola iteración, con entregables verificables al finalizar cada historia
   de usuario.

2. **IA Generativa:** Claude Code demostró ser una herramienta efectiva para acelerar el
   desarrollo sin sacrificar calidad. Redujo el tiempo estimado de desarrollo de semanas
   a horas, generando código limpio, modular y documentado.

3. **Manejo de excepciones:** Se implementó en cuatro niveles (formularios, vistas,
   calculadora y control de acceso), garantizando que ninguna operación inválida llegue
   a afectar la base de datos o exponer datos sensibles.

4. **Código limpio:** La aplicación de los principios de Robert C. Martin resultó en un
   código modular, legible y fácilmente extensible para futuros módulos del sistema.

5. **Repositorio:** El proyecto está alojado en GitHub con historial de versiones y
   disponible para revisión en: https://github.com/JTRAVE/sysaco

---

## REFERENCIAS

- Beck, K. et al. (2001). *Manifesto for Agile Software Development*. agilemanifesto.org
- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall.
- Schwaber, K. & Sutherland, J. (2020). *The Scrum Guide*. scrumguides.org
- Django Software Foundation. (2024). *Django 5.2 Documentation*. djangoproject.com
- Anthropic. (2025). *Claude Code Documentation*. anthropic.com
- SUNAT. (2025). *UIT 2025: S/ 5,350*. R.M. 000395-2024-EF.
- Ministerio de Trabajo. (2024). *SMV: S/ 1,025*. D.U. 010-2024.
