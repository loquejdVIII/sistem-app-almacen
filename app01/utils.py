from django.urls import path
from app01 import views
from django.core.exceptions import PermissionDenied

def es_administrador(user):
    return user.groups.filter(name='Administrador').exists()

def administrador_requerido(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if es_administrador(request.user):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view_func