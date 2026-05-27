"""
Calculadora de planilla según normativa laboral peruana vigente.
Decreto Supremo N° 003-97-TR (TUO Ley de Productividad y Competitividad Laboral)
"""
from decimal import Decimal, ROUND_HALF_UP


# --- Valores normativos vigentes ---
SMV = Decimal('1025.00')       # Sueldo Mínimo Vital (D.U. 010-2024)
UIT = Decimal('5350.00')       # UIT 2025 (R.M. 000395-2024-EF)
TASA_ESSALUD = Decimal('0.09')
TASA_ONP = Decimal('0.13')
TASA_AFP_FONDO = Decimal('0.10')
TASA_AFP_COMISION = Decimal('0.0147')   # comisión flujo promedio
TASA_AFP_SEGURO = Decimal('0.0135')     # prima de seguro promedio
TASA_ASIG_FAMILIAR = Decimal('0.10')


def redondear(valor):
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calcular_asignacion_familiar(tiene_familia: bool) -> Decimal:
    if tiene_familia:
        return redondear(SMV * TASA_ASIG_FAMILIAR)
    return Decimal('0.00')


def calcular_remuneracion_bruta(sueldo_basico: Decimal, asignacion_familiar: Decimal) -> Decimal:
    return redondear(sueldo_basico + asignacion_familiar)


def calcular_essalud(remuneracion_bruta: Decimal) -> Decimal:
    """Aporte del empleador al EsSalud (9%). Mínimo sobre SMV."""
    base = max(remuneracion_bruta, SMV)
    return redondear(base * TASA_ESSALUD)


def calcular_aporte_onp(remuneracion_bruta: Decimal) -> Decimal:
    return redondear(remuneracion_bruta * TASA_ONP)


def calcular_aporte_afp(remuneracion_bruta: Decimal) -> dict:
    fondo = redondear(remuneracion_bruta * TASA_AFP_FONDO)
    comision = redondear(remuneracion_bruta * TASA_AFP_COMISION)
    seguro = redondear(remuneracion_bruta * TASA_AFP_SEGURO)
    total = redondear(fondo + comision + seguro)
    return {'fondo': fondo, 'comision': comision, 'seguro': seguro, 'total': total}


def calcular_gratificacion(remuneracion_bruta: Decimal) -> dict:
    """
    Gratificación semestral (julio y diciembre).
    Ley 27735 — equivale a 1 remuneración por semestre completo.
    Bonificación extraordinaria: 9% sobre la gratificación (Ley 29351).
    """
    gratificacion = redondear(remuneracion_bruta)
    bonificacion_ext = redondear(gratificacion * TASA_ESSALUD)
    mensualizado = redondear(gratificacion / Decimal('6'))
    return {
        'semestral': gratificacion,
        'bonificacion_extraordinaria': bonificacion_ext,
        'mensualizado': mensualizado,
    }


def calcular_cts(remuneracion_bruta: Decimal, gratificacion_semestral: Decimal) -> dict:
    """
    CTS mensual — Decreto Legislativo 650.
    Base = Remuneración + (1/6 gratificación semestral).
    Depósito semestral en mayo (por ene-abr) y noviembre (por may-oct).
    """
    base_cts = redondear(remuneracion_bruta + redondear(gratificacion_semestral / Decimal('6')))
    mensual = redondear(base_cts / Decimal('12'))
    semestral = redondear(mensual * Decimal('6'))
    return {'base': base_cts, 'mensual': mensual, 'semestral': semestral}


def calcular_vacaciones(remuneracion_bruta: Decimal) -> Decimal:
    """Vacaciones: 30 días al año = 1 remuneración mensual (Art. 10 Ley 27671)."""
    return redondear(remuneracion_bruta / Decimal('12'))


def calcular_ir_5ta_categoria(remuneracion_bruta: Decimal, gratificacion_semestral: Decimal) -> dict:
    """
    Impuesto a la Renta 5ta Categoría — Art. 75 LIR.
    Proyección anual: (remuneración * 12) + 2 gratificaciones.
    Deducción: 7 UIT.
    Tasas progresivas acumulativas (Art. 53 LIR).
    """
    renta_bruta_anual = redondear(remuneracion_bruta * 12 + gratificacion_semestral * 2)
    deduccion = redondear(UIT * Decimal('7'))
    renta_neta_anual = max(renta_bruta_anual - deduccion, Decimal('0.00'))

    tramos = [
        (UIT * 5,  Decimal('0.08')),
        (UIT * 20, Decimal('0.14')),
        (UIT * 35, Decimal('0.17')),
        (UIT * 45, Decimal('0.20')),
        (None,     Decimal('0.30')),
    ]

    ir_anual = Decimal('0.00')
    tope_anterior = Decimal('0.00')
    detalle_tramos = []

    for tope, tasa in tramos:
        if renta_neta_anual <= tope_anterior:
            break
        limite = tope if tope is not None else renta_neta_anual
        base_tramo = min(renta_neta_anual, limite) - tope_anterior
        impuesto_tramo = redondear(base_tramo * tasa)
        if base_tramo > 0:
            detalle_tramos.append({
                'desde': tope_anterior,
                'hasta': min(renta_neta_anual, limite),
                'tasa': tasa * 100,
                'impuesto': impuesto_tramo,
            })
        ir_anual += impuesto_tramo
        tope_anterior = limite

    ir_anual = redondear(ir_anual)
    retencion_mensual = redondear(ir_anual / Decimal('12'))

    return {
        'renta_bruta_anual': renta_bruta_anual,
        'deduccion_7uit': deduccion,
        'renta_neta_anual': renta_neta_anual,
        'ir_anual': ir_anual,
        'retencion_mensual': retencion_mensual,
        'tramos': detalle_tramos,
    }


def calcular_planilla_completa(sueldo_basico: Decimal, tiene_familia: bool, tipo_pension: str) -> dict:
    """Calcula todos los conceptos de planilla para un empleado."""
    asig_familiar = calcular_asignacion_familiar(tiene_familia)
    rem_bruta = calcular_remuneracion_bruta(sueldo_basico, asig_familiar)
    essalud = calcular_essalud(rem_bruta)
    gratificacion = calcular_gratificacion(rem_bruta)
    cts = calcular_cts(rem_bruta, gratificacion['semestral'])
    vacaciones = calcular_vacaciones(rem_bruta)
    ir = calcular_ir_5ta_categoria(rem_bruta, gratificacion['semestral'])

    if tipo_pension == 'AFP':
        pension = calcular_aporte_afp(rem_bruta)
        descuento_pension = pension['total']
    else:
        pension = {'total': calcular_aporte_onp(rem_bruta)}
        descuento_pension = pension['total']

    total_descuentos = redondear(descuento_pension + ir['retencion_mensual'])
    remuneracion_neta = redondear(rem_bruta - total_descuentos)

    costo_total_empleador = redondear(rem_bruta + essalud + gratificacion['mensualizado'] + cts['mensual'])

    return {
        'sueldo_basico': sueldo_basico,
        'asignacion_familiar': asig_familiar,
        'remuneracion_bruta': rem_bruta,
        # Descuentos del trabajador
        'pension': pension,
        'tipo_pension': tipo_pension,
        'ir_5ta': ir,
        'total_descuentos': total_descuentos,
        'remuneracion_neta': remuneracion_neta,
        # Aportes del empleador
        'essalud': essalud,
        # Beneficios sociales
        'gratificacion': gratificacion,
        'cts': cts,
        'vacaciones': vacaciones,
        # Costo total empleador (mensualizado)
        'costo_total_empleador': costo_total_empleador,
        # Referencia normativa
        'smv': SMV,
        'uit': UIT,
    }
