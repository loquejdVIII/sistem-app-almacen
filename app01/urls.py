from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from app01 import views

urlpatterns = [
#    path('login/', auth_views.LoginView.as_view(), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.principal, name="principal"),
    path('salir/', views.salir, name="salir"),
    path('seleccionar-ruta/', views.seleccionar_ruta, name='seleccionar_ruta'),
    path('administrar-codigos/', views.administrar_codigos, name='administrar_codigos')
]