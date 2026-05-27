from django.urls import path
from . import views

app_name = 'planilla'

urlpatterns = [
    path('', views.lista_planillas, name='lista'),
    path('calculadora/', views.calculadora_rapida, name='calculadora'),
    path('nuevo/', views.crear_registro, name='crear'),
    path('<int:pk>/', views.detalle_registro, name='detalle'),
    path('<int:pk>/eliminar/', views.eliminar_registro, name='eliminar'),
    path('empleado/<int:pk>/boleta/', views.boleta_empleado, name='boleta_empleado'),
]
