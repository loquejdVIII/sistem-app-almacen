from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .management.commands.monitor import start_monitoring, stop_monitoring
from .models import nombreEtiqueta, lecturaRFID, seleccionarRuta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
import threading
from django.contrib import messages

def es_administrador(user):
    return user.groups.filter(name='Administrador').exists()

# Variables globales para el monitor y el hilo
monitor = None
monitor_thread = None

@login_required
@csrf_exempt
def control_monitor_view(request):
    global monitor, monitor_thread
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'start':
            if monitor is None:  # Asegúrate de que el monitor no esté ya en ejecución
                monitor = start_monitoring()
                if monitor:
                    # Crear un hilo para el monitor y arrancarlo
                    monitor_thread = threading.Thread(target=keep_monitor_running)
                    monitor_thread.start()
                    return JsonResponse({"status": "success", "message": "Monitoreo iniciado"})
                else:
                    return JsonResponse({"status": "error", "message": "No se encontró la ruta de la carpeta"})
            else:
                return JsonResponse({"status": "error", "message": "El monitoreo ya está en ejecución"})
        elif action == 'stop':
            if monitor:
                stop_monitoring(monitor)
                monitor = None
                monitor_thread.join()  # Esperar a que el hilo termine
                return JsonResponse({"status": "success", "message": "Monitoreo detenido"})
            else:
                return JsonResponse({"status": "error", "message": "No hay monitoreo en ejecución"})
        elif action == 'update':
            # Implementa la lógica para actualizar los datos aquí
            # Ejemplo: refrescar los datos desde la fuente
            return JsonResponse({"status": "success", "message": "Datos actualizados"})
        elif action == 'clear':
            lecturaRFID.objects.all().delete()
            return JsonResponse({"status": "success", "message": "Datos limpiados"})
    
    return JsonResponse({"status": "error", "message": "Acción no válida"})

def keep_monitor_running():
    while monitor:
        pass  # Mantener el monitor en ejecución

def monitor_status_view(request):
    if monitor:
        return JsonResponse({"status": "running"})
    else:
        return JsonResponse({"status": "stopped"})

@login_required
def principal(request):

    lecturas = lecturaRFID.objects.all()
    herramientas = nombreEtiqueta.objects.all()
    verificar_ruta = seleccionarRuta.objects.first()
        
    if verificar_ruta:
        ruta = verificar_ruta.carpeta_excel
        lecturas = lecturaRFID.objects.all()
        herramientas = nombreEtiqueta.objects.all()
        total_herramientas = len(lecturas)
    else:
        # Si no hay configuración definida, inicializamos las variables con valores predeterminados
        ruta = ""

    # Obtener el número total de herramientas
    total_herramientas = len(lecturas)

    # Asociar los nombres de herramientas a las lecturas
    for lectura in lecturas:
        lectura.asociar_nombre_herramienta()
    
    # Filtrar las lecturas si se envió el formulario de filtro
    herramienta_seleccionada = request.GET.get('herramienta')
    fecha_creacion = request.GET.get('fecha_creacion')

    if herramienta_seleccionada:
        lecturas = lecturas.filter(nombre_herramienta=herramienta_seleccionada)

    if fecha_creacion:
        # Convertir la fecha del formulario a formato datetime
        fecha_creacion = datetime.strptime(fecha_creacion, "%Y-%m-%d").date()
        # Filtrar las lecturas por fecha de creación ignorando la hora
        lecturas = lecturas.filter(fecha_modificacion__date=fecha_creacion)

    total_disponibles = lecturas.filter(estado='disponible').count()
    total_no_disponibles_obra = lecturas.filter(estado='no_disponible_obra').count()
    total_no_disponibles_malogrado = lecturas.filter(estado='no_disponible_malogrado').count()
    total_no_especificado = lecturas.filter(estado='no_especificado').count()

    herramienta_busq = lecturaRFID.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        herramienta_busq = herramienta_busq.filter(tag_id=search_query)

    # Renderizar el template con los datos de las lecturas y herramientas
    return render(request, 'principal.html', {
        'lecturas': lecturas,
        'total_herramientas': total_herramientas,
        'herramientas': herramientas,
        'ruta': ruta,
        'total_disponibles': total_disponibles,
        'total_no_disponibles_obra': total_no_disponibles_obra,
        'total_no_disponibles_malogrado': total_no_disponibles_malogrado,
        'total_no_especificado': total_no_especificado,
        'herramienta_busq': herramienta_busq,
        'search_query': search_query,
        'es_administrador': es_administrador(request.user),
    })

@login_required
def modificar_estado(request):
    herramienta = None
    if request.method == 'POST':
        if 'buscar' in request.POST:
            tag_id = request.POST.get('tag_id')
            herramientas = lecturaRFID.objects.filter(tag_id=tag_id)
            if herramientas.exists():
                herramienta = herramientas.first()  # Obtener el primer resultado
            else:
                messages.error(request, f'No se encontró ninguna herramienta con el ID {tag_id}.')
        elif 'modificar' in request.POST:
            tag_id = request.POST.get('tag_id')
            nuevo_estado = request.POST.get('estado')
            herramientas = lecturaRFID.objects.filter(tag_id=tag_id)
            if herramientas.exists():
                herramienta = herramientas.first()  # Obtener el primer resultado
                herramienta.estado = nuevo_estado
                herramienta.save()
                messages.success(request, f'El estado de la herramienta con ID {tag_id} ha sido modificado a {nuevo_estado}.')
            else:
                messages.error(request, f'No se encontró ninguna herramienta con el ID {tag_id}.')

    return render(request, 'modificar_estado.html', {
        'herramienta': herramienta,
    })

@login_required
def seleccionar_ruta(request):
    if request.method == 'POST':
        captura_ruta = request.POST.get('nueva_ruta', '') 
        if captura_ruta:
            ruta_existe = seleccionarRuta.objects.first()
            if ruta_existe:
                ruta_existe.carpeta_excel = captura_ruta
                ruta_existe.save()
            else:
                nueva_ruta = seleccionarRuta(carpeta_excel=captura_ruta)
                nueva_ruta.save()
        return redirect('principal')
    return render(request, 'seleccionar_ruta.html')

@login_required
def administrar_codigos(request):
    if request.method == 'POST':
        etiqueta_id = request.POST.get('etiqueta_id')
        nombre_herramienta = request.POST.get('nombre_herramienta')
        confirmacion = request.POST.get('confirmacion')

        # Buscar si existe una etiqueta con ese ID
        etiqueta = nombreEtiqueta.objects.filter(etiqueta_id=etiqueta_id).first()
        
        if etiqueta and not confirmacion:
            mensaje = "La etiqueta ya existe con el nombre '{}'.".format(etiqueta.nombre_herramienta)
            advertencia = "Está a punto de cambiar el nombre de una etiqueta existente. ¿Está seguro de continuar?"
            return render(request, 'administrar_codigos.html', {
                'mensaje': mensaje,
                'advertencia': advertencia,
                'etiqueta_id': etiqueta_id,
                'nombre_herramienta': nombre_herramienta,
                'mostrar_confirmacion': True,
            })
        
        etiqueta, created = nombreEtiqueta.objects.update_or_create(
            etiqueta_id=etiqueta_id,
            defaults={'nombre_herramienta': nombre_herramienta},
        )
        
        if created:
            mensaje = "Etiqueta creada exitosamente."
        else:
            mensaje = "Etiqueta actualizada exitosamente."
        
        return render(request, 'administrar_codigos.html', {'mensaje': mensaje})
    
    return render(request, 'administrar_codigos.html')

@login_required
def salir(request):
    logout(request)
    return redirect('/')