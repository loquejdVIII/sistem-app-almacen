from django.shortcuts import redirect, render
from .management.commands.leedor_excel import detener_lectura_carpeta, leer_excel_view
from .models import nombreEtiqueta, lecturaRFID, seleccionarRuta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required

def principal(request):

    lecturas = lecturaRFID.objects.all()
    herramientas = nombreEtiqueta.objects.all()
    verificar_ruta = seleccionarRuta.objects.first()
    
    if request.method == 'POST':
        if 'leer_datos' in request.POST:
            print("se presiono leer datos")
            if verificar_ruta and verificar_ruta.carpeta_excel:
                print("se ejecuta la lectura")
                leer_excel_view(request)
            else:
                # Si la carpeta de Excel no está especificada, mostrar un mensaje de advertencia
                mensaje_error = "No se puede leer datos porque no se ha especificado la ruta de la carpeta de lectura."
                return render(request, 'principal.html', {'mensaje_error': mensaje_error})
        elif 'limpiar_datos' in request.POST:
            # Eliminar todas las lecturas RFID de herramientas
            lecturaRFID.objects.all().delete()
            # Redireccionar a la misma página
        elif 'detener_lectura' in request.POST:
            print("se detiene la lectura")
            detener_lectura_carpeta()       
        
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
    if herramienta_seleccionada:
        lecturas = lecturas.filter(nombre_herramienta=herramienta_seleccionada)

    # Renderizar el template con los datos de las lecturas y herramientas
    return render(request, 'principal.html', {
        'lecturas': lecturas,
        'total_herramientas': total_herramientas,
        'herramientas': herramientas,
        'ruta': ruta,
    })
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

def administrar_codigos(request):
    # Verificar si se envió el formulario
    if request.method == 'POST':
        # Obtener los datos del formulario
        etiqueta_id = request.POST.get('etiqueta_id')
        nombre_herramienta = request.POST.get('nombre_herramienta')
        
        # Guardar los datos en la base de datos
        nuevo_codigo = nombreEtiqueta(etiqueta_id=etiqueta_id, nombre_herramienta=nombre_herramienta)
        nuevo_codigo.save()
        
        # Renderizar la plantilla con el mensaje de confirmación
        return render(request, 'administrar_codigos.html', {'datos_guardados': True})

    # Si no se envió el formulario, mostrar la página normalmente
    return render(request, 'administrar_codigos.html')

def salir(request):
    logout(request)
    return redirect('/')