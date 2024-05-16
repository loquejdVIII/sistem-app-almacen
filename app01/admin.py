from django.contrib import admin
from .models import nombreEtiqueta, lecturaRFID, seleccionarRuta
# from .forms import ConfiguracionForm

admin.site.register(nombreEtiqueta)
admin.site.register(lecturaRFID)
admin.site.register(seleccionarRuta)

# @admin.register(CodigoTagID)
# class CodigoTagIDAdmin(admin.ModelAdmin):
#     list_display = ('tag_id', 'nombre_herramienta')
#     search_fields = ('tag_id', 'nombre_herramienta')
# @admin.register(Configuracion)
# class ConfiguracionAdmin(admin.ModelAdmin):
#     verbose_name = "Ruta de carpeta"  # Cambia este nombre a tu preferencia
#    form = ConfiguracionForm