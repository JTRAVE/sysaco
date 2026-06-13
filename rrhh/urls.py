from django.urls import path
from . import views

app_name = 'rrhh'

urlpatterns = [
    path('', views.dashboard_rrhh, name='lista'),
    path('empleados/', views.lista_empleados, name='empleados'),
    path('nuevo/', views.crear_empleado, name='crear'),
    path('<int:pk>/editar/', views.editar_empleado, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_empleado, name='eliminar'),
    path('<int:pk>/', views.detalle_empleado, name='detalle'),
]
