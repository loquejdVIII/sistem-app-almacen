from django.urls import path
from app01 import views

urlpatterns = [
    path('', views.principal, name="principal"),
    path('control-monitor/', views.control_monitor_view, name='control_monitor'),
    path('monitor-status/', views.monitor_status_view, name='monitor_status'),
    path('seleccionar-ruta/', views.seleccionar_ruta, name='seleccionar_ruta'),
    path('modificar-estado/', views.modificar_estado, name='modificar_estado'),
    # path('modificar-estado/<int:lectura_id>/', views.modificar_estado, name='modificar_estado'),
    path('administrar-codigos/', views.administrar_codigos, name='administrar_codigos'),
    path('salir/', views.salir, name="salir"),
]