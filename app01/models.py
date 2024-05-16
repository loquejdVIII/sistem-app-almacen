from django.db import models

class nombreEtiqueta(models.Model):
    etiqueta_id = models.CharField(max_length=100, unique=True)
    nombre_herramienta = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_herramienta
      
    class Meta:
        verbose_name_plural = "Identificadores de etiquetas de códigos"
        verbose_name = "un identificador de etiqueta de codigo"

class lecturaRFID(models.Model):
#    models.DateTimeField()
    tiempo = models.CharField(max_length=8)
    tag_id = models.CharField(max_length=24)
    length = models.IntegerField()
    ant = models.IntegerField()
    cnt = models.IntegerField()
    rssi = models.IntegerField()
    nombre_herramienta = models.CharField(max_length=100, blank=True, null=True)

    def asociar_nombre_herramienta(self):
        try:
# Intenta encontrar una instancia de CodigoTagID que coincida con el tag_id de la lecturaRFID
            union_tag_nom = nombreEtiqueta.objects.get(etiqueta_id=self.tag_id)
# Si se encuentra una instancia, asigna el nombre de la herramienta de esa instancia a la lecturaRFID
            self.nombre_herramienta = union_tag_nom.nombre_herramienta
# Guarda los cambios a la base de datos
            self.save()
        except nombreEtiqueta.DoesNotExist:
# Si no se encuentra una instancia, asigna "Desconocido" como nombre de la herramienta
            self.nombre_herramienta = "Desconocido"
        
    class Meta:
        verbose_name_plural = "Lecturas RFID de herramientas"
        verbose_name = "una nueva lectura RFID"
    
    def __str__(self):
        return f"Lectura de TagID: {self.tag_id} en {self.tiempo}"

class seleccionarRuta(models.Model):
    carpeta_excel = models.CharField(max_length=255)

    def __str__(self):
        return "config"
    
    class Meta:
        verbose_name_plural = "Configuración de la ruta de lectura"
        verbose_name = "la ruta de lectura"