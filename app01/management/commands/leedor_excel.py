from app01.models import seleccionarRuta, lecturaRFID
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

observer = None

class ExcelHandler(FileSystemEventHandler):
    def __init__(self, carpeta_excel):
        super().__init__()
        self.carpeta_excel = carpeta_excel

    def on_created(self, event):
        # Cuando se crea un nuevo archivo, lo procesamos
        if event.is_directory:
            return
        if event.event_type == 'created':
            # Procesar el archivo Excel recién creado
            procesar_excel(event.src_path, self.carpeta_excel)

def hex_to_decimal(hex_string):
    # Eliminar el prefijo '0x' si está presente
    hex_string = hex_string.replace("0x", "")
    # Convertir de hexadecimal a decimal
    return int(hex_string, 16)

def procesar_excel(archivo, carpeta_excel):
    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo)
        
        # Iterar sobre cada fila del DataFrame
        for index, row in df.iterrows():
            # Convertir las columnas de longitud (length) y rssi de hexadecimal a decimal
            length_decimal = hex_to_decimal(row['Length'])
            rssi_decimal = hex_to_decimal(row['RSSI'])

            # Crear una instancia de lecturaRFID con los datos de la fila
            nueva_lectura = lecturaRFID(
                tiempo=row['Time'],
                tag_id=row['TagID'],
                length=length_decimal,
                ant=row['Ant'],
                cnt=row['Cnt'],
                rssi=rssi_decimal
            )
            # Guardar la instancia en la base de datos
            nueva_lectura.save()

        # Indicar que el archivo Excel se procesó exitosamente
        print(f'Archivo Excel "{archivo}" leído y datos almacenados en la base de datos')
    except Exception as e:
        # Manejar cualquier error que ocurra durante el proceso
        print(f'Error al procesar el archivo Excel "{archivo}": {e}')

def leer_excel_view(request):
    # Obtener la ruta de la carpeta Excel de la base de datos
    ruta = seleccionarRuta.objects.first()
    carpeta_excel = ruta.carpeta_excel

    # Monitorear la carpeta para procesar los archivos Excel
    monitorear_carpeta(carpeta_excel)

def monitorear_carpeta(carpeta_excel):
    global observer
    event_handler = ExcelHandler(carpeta_excel)
    observer = Observer()
    observer.schedule(event_handler, carpeta_excel, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def detener_lectura_carpeta():
    global observer
    if observer:
        observer.stop()
        observer.join()