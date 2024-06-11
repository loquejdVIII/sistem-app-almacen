from django.db import models

class nombreEtiqueta(models.Model):
    etiqueta_id = models.CharField(max_length=100, unique=True)
    nombre_herramienta = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_herramienta
      
    class Meta:
        verbose_name_plural = "Nombres de herramientas según su ID"
        verbose_name = "Nombre de herramienta según su ID"

class lecturaRFID(models.Model):
#    models.DateTimeField()
    ESTADOS_HERRAMIENTA = [
        ('no_especificado', 'No especificado'),
        ('disponible', 'Disponible'),
        ('no_disponible_obra', 'No disponible (en obra)'),
        ('no_disponible_malogrado', 'No disponible (malogrado)'),
    ]
    tiempo = models.CharField(max_length=8)
    tag_id = models.CharField(max_length=24)
    length = models.CharField(max_length=10)
    ant = models.IntegerField()
    cnt = models.IntegerField()
    rssi = models.CharField(max_length=10)
    nombre_archivo = models.CharField(max_length=255)
    fecha_modificacion = models.DateTimeField()
    nombre_herramienta = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=23, choices=ESTADOS_HERRAMIENTA, default='disponible')

    def hex_value(self, value):
        try:
            return hex(int(value))
        except ValueError:
            return ''

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
        return f"Lectura RFID - ID: {self.tag_id}, Tiempo: {self.tiempo}, Estado: {self.estado}, Nombre de la herramienta asignado: {self.nombre_herramienta if self.nombre_herramienta else 'No asignado'}"

class seleccionarRuta(models.Model):
    carpeta_excel = models.CharField(max_length=255)

    def __str__(self):
        return "carpeta_excel"
    
    class Meta:
        verbose_name_plural = "Configuración de la ruta de lectura"
        verbose_name = "la ruta de lectura"