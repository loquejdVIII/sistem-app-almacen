import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import django
from django.conf import settings
from app01.models import seleccionarRuta, lecturaRFID

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

class ExcelHandler(FileSystemEventHandler):
    def __init__(self, folder_to_watch):
        self.folder_to_watch = folder_to_watch
        self.observer = Observer()
    
    def start(self):
        self.observer.schedule(self, self.folder_to_watch, recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def on_created(self, event):
        if event.is_directory:
            return None

        if event.src_path.endswith('.xls'):
            self.process_file(event.src_path)

    def process_file(self, file_path):
        # Leer el archivo Excel
        df = pd.read_excel(file_path)

        # Obtener la fecha de modificación del archivo
        fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(file_path))

        # Procesar cada fila del DataFrame
        for index, row in df.iterrows():
            # Crear una instancia del modelo lecturaRFID
            lectura = lecturaRFID(
                tiempo=row['Time'],
                tag_id=row['TagID'],
                length=row['Length'],
                ant=row['Ant'],
                cnt=row['Cnt'],
                rssi=row['RSSI'],
                nombre_archivo=os.path.basename(file_path),
                fecha_modificacion=fecha_modificacion,
            )
            # lectura.asociar_nombre_herramienta()  # Asociar nombre de herramienta si aplica
            lectura.save()

        print(f"Archivo procesado y guardado: {file_path}")

# Funciones para controlar el script
def start_monitoring():
    # Obtener la ruta de la carpeta desde el modelo seleccionarRuta
    ruta_obj = seleccionarRuta.objects.first()
    if not ruta_obj:
        print("No se ha encontrado una ruta configurada en la base de datos.")
        return None
    
    folder_path = ruta_obj.carpeta_excel
    event_handler = ExcelHandler(folder_path)
    event_handler.start()
    return event_handler

def stop_monitoring(event_handler):
    event_handler.stop()