"""
Pruebas unitarias para el módulo RRHH.
Proyecto SYSACO — Construcción de Software
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class EmpleadoViewsTest(TestCase):
    """Pruebas para las vistas del módulo RRHH."""

    def setUp(self):
        """Configurar usuario de prueba y cliente autenticado."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_dashboard_rrhh_requiere_autenticacion(self):
        """Una sesión sin autenticar debe redirigir al login."""
        self.client.logout()
        response = self.client.get(reverse('rrhh:lista'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_dashboard_rrhh_autenticado(self):
        """Un usuario autenticado debe ver el dashboard de Capital Humano."""
        response = self.client.get(reverse('rrhh:lista'))
        self.assertEqual(response.status_code, 200)

    def test_lista_empleados_requiere_autenticacion(self):
        """Una sesión sin autenticar debe redirigir al login."""
        self.client.logout()
        response = self.client.get(reverse('rrhh:empleados'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_lista_empleados_autenticado(self):
        """Un usuario autenticado debe ver la lista de empleados."""
        response = self.client.get(reverse('rrhh:empleados'))
        self.assertEqual(response.status_code, 200)

    def test_crear_empleado_requiere_autenticacion(self):
        """El formulario de nuevo empleado exige sesión activa."""
        self.client.logout()
        response = self.client.get(reverse('rrhh:crear'))
        self.assertEqual(response.status_code, 302)

    def test_crear_empleado_get_autenticado(self):
        """Un usuario autenticado debe ver el formulario de alta."""
        response = self.client.get(reverse('rrhh:crear'))
        self.assertEqual(response.status_code, 200)
