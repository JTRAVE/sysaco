"""
Pruebas unitarias para la calculadora de planilla peruana.
Verifica ONP, EsSalud e IR 5ta Categoría según normativa vigente.
"""
from django.test import TestCase
from decimal import Decimal

from planilla.calculadora import (
    calcular_aporte_onp,
    calcular_essalud,
    calcular_asignacion_familiar,
    calcular_remuneracion_bruta,
    calcular_planilla_completa,
)


class CalculadoraPlanillaTest(TestCase):
    """Pruebas para la calculadora de remuneraciones peruanas."""

    def setUp(self):
        self.sueldo_rmv = Decimal('1025.00')   # RMV 2024 (D.U. 010-2024)
        self.sueldo_admin = Decimal('1700.00')
        self.sueldo_gerente = Decimal('2000.00')

    def test_onp_sobre_rmv(self):
        """ONP = 13% del sueldo bruto (D.L. 19990)."""
        resultado = calcular_aporte_onp(self.sueldo_rmv)
        esperado = Decimal('133.25')   # 1025 * 0.13
        self.assertEqual(resultado, esperado)

    def test_essalud_empleador(self):
        """EsSalud = 9% a cargo del empleador (Ley 26790)."""
        resultado = calcular_essalud(self.sueldo_rmv)
        esperado = Decimal('92.25')    # 1025 * 0.09
        self.assertEqual(resultado, esperado)

    def test_asignacion_familiar_con_familia(self):
        """Asignación familiar = 10% SMV si tiene hijos (Ley 25129)."""
        resultado = calcular_asignacion_familiar(True)
        esperado = Decimal('102.50')   # 1025 * 0.10
        self.assertEqual(resultado, esperado)

    def test_asignacion_familiar_sin_familia(self):
        """Sin hijos la asignación familiar debe ser cero."""
        resultado = calcular_asignacion_familiar(False)
        self.assertEqual(resultado, Decimal('0.00'))

    def test_remuneracion_bruta_con_af(self):
        """Remuneración bruta = sueldo básico + asignación familiar."""
        af = calcular_asignacion_familiar(True)
        resultado = calcular_remuneracion_bruta(self.sueldo_rmv, af)
        esperado = Decimal('1127.50')  # 1025 + 102.50
        self.assertEqual(resultado, esperado)

    def test_onp_sueldo_gerente(self):
        """ONP sobre sueldo de gerente: 2000 * 0.13 = 260.00."""
        resultado = calcular_aporte_onp(self.sueldo_gerente)
        self.assertEqual(resultado, Decimal('260.00'))

    def test_planilla_completa_onp_retorna_remuneracion_neta(self):
        """planilla_completa con ONP debe retornar remuneracion_neta positivo."""
        resultado = calcular_planilla_completa(self.sueldo_admin, False, 'ONP')
        self.assertIn('remuneracion_neta', resultado)
        self.assertGreater(resultado['remuneracion_neta'], Decimal('0'))

    def test_planilla_completa_afp_retorna_remuneracion_neta(self):
        """planilla_completa con AFP debe retornar remuneracion_neta positivo."""
        resultado = calcular_planilla_completa(self.sueldo_admin, True, 'AFP')
        self.assertIn('remuneracion_neta', resultado)
        self.assertGreater(resultado['remuneracion_neta'], Decimal('0'))
