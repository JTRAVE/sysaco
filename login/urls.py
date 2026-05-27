from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),   # http://127.0.0.1:8000/login/
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
