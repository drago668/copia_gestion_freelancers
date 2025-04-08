from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion.forms import UsuarioForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from .models import Proyecto,Contrato
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomAuthenticationForm, PerfilForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Tarea, SeguimientoTiempo
from django.utils.timezone import now
from .forms import TareaForm

@login_required
def crear_tarea(request, proyecto_id):
    # Asegurarse de que el proyecto pertenezca al usuario actual
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id, id_usuario=request.user)
    
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.id_proyecto = proyecto  # Asigna el proyecto a la tarea
            tarea.save()
            # Redirige a la vista de detalle del proyecto o a la lista de tareas
            return redirect('seguimiento_tareas')
        else:
            # Si el formulario no es válido, retornamos la misma plantilla con errores
            return render(request, 'crear_tarea.html', {'form': form, 'proyecto': proyecto})
    else:
        form = TareaForm()
    
    return render(request, 'seguimiento_tareas.html', {'form': form, 'proyecto': proyecto})

@login_required
def index(request):
    return render(request, 'index.html')
@login_required
def contrato(request): #aqui se configuran la logica para visulaizar los contratos
    return render(request,'contrato.html')
@login_required
def proyecto(request):
    return render(request, 'proyecto.html')
@login_required
def tiempo(request):
    return render(request,'tiempo.html')
@login_required
def perfil(request):
    proyectos = Proyecto.objects.filter(id_usuario=request.user)
    gestion_contratos = Contrato.objects.filter(id_usuario=request.user)
    return render(request, 'perfil.html', {"proyectos": proyectos,"contratos": gestion_contratos})
    
def login_view(request):
    print("ingresooo")
    if request.method == 'POST':
        print("Se recibió una solicitud POST")
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("El formulario es valido")
            user = form.get_user()
            login(request, user)
            return redirect('inicio')  # O la página a la que quieras redirigir después de iniciar sesión
        else:
            print("El formulario es invalido")
        
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def registrar(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()  # Crea el usuario pero no lo guarda
            login(request, user)
            return redirect('inicio')
    else:
        form = UsuarioForm()
    return render(request, 'registro.html', {'form': form})


@login_required
def gestion_contratos(request):
    if request.method == "POST":
        print("olicitud post hecha")
        nombre_cliente = request.POST.get("nombre_cliente")
        descripcion = request.POST.get("descripcion_servicio")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        monto=request.POST.get("monto")
        terminos=request.POST.get("terminos")
        #monto_acordado = request.POST.get("monto")  # Campo corregido

        if nombre_cliente and fecha_inicio and fecha_fin:
            Contrato.objects.create(
                id_usuario=request.user,
                nombre_cliente=nombre_cliente,
                monto= monto,
                terminos=terminos,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
            )
            #return JsonResponse({"mensaje": "Contrato creado exitosamente"}, status=201)
        else:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)
    if request.method == "GET":
        gestion_contratos = Contrato.objects.filter(id_usuario=request.user)
        print("solicitud get hecha")

    gestion_contratos = Contrato.objects.filter(id_usuario=request.user)
    return render(request, "gestion_contratos.html", {"contratos": gestion_contratos})

def salir(request):
    logout(request)
    return redirect(request,'index.html')

@login_required
def proyectos(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")

        if nombre and fecha_inicio and fecha_fin:
            Proyecto.objects.create(
                id_usuario=request.user,
                nombre=nombre,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
        else:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)
    if request.method == "GET":proyectos = Proyecto.objects.filter(id_usuario=request.user)
    
    proyectos = Proyecto.objects.filter(id_usuario=request.user)
    return render(request, "proyectos.html", {"proyectos": proyectos})

@login_required
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id, id_usuario=request.user)
    
    if request.method == "POST":
        proyecto.nombre= request.POST.get("nombre")
        proyecto.descripcion = request.POST.get("descripcion")
        proyecto.fecha_inicio = request.POST.get("fecha_inicio")
        proyecto.fecha_fin = request.POST.get("fecha_fin")
        proyecto.save()
        return redirect('proyectos')  # O donde tengas la lista de contratos
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id, id_usuario=request.user)
    if request.method == "POST":
        proyecto.delete()
        return redirect('proyectos')
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def subir_foto_perfil(request):
    if request.method == 'POST':
        print("se ha recibido solicitud post")
        # Verifica si el archivo se encuentra en request.FILES
        if 'profile_picture' in request.FILES:
            print("Se encuentra imagen")
            # Obtiene el archivo
            archivo = request.FILES['profile_picture']
            # Actualiza el campo del usuario
            request.user.imagen = archivo  # O request.user.imagen si usas ese nombre
            request.user.save()
            return redirect('perfil')  # O la URL que desees redireccionar tras actualizar
        else:
            return HttpResponse("No se encontró el archivo.", status=400)
    else:
        return render(request, 'perfil.html')  # O la plantilla que uses para editar perfil


@csrf_exempt
def actualizar_estado_proyecto(request, proyecto_id):
    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")

        if nuevo_estado in ["pendiente", "en_proceso", "terminado"]:
            try:
                proyecto = Proyecto.objects.get(id_proyecto=proyecto_id)
                proyecto.estado = nuevo_estado
                proyecto.save()
                return JsonResponse({"mensaje": "Estado actualizado correctamente"}, status=200)
            except Proyecto.DoesNotExist:
                return JsonResponse({"error": "Proyecto no encontrado"}, status=404)
        else:
            return JsonResponse({"error": "Estado no válido"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def editar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id_contrato=contrato_id, id_usuario=request.user)
    
    if request.method == "POST":
        contrato.nombre_cliente = request.POST.get("nombre_cliente")
        contrato.descripcion = request.POST.get("descripcion_servicio")
        contrato.fecha_inicio = request.POST.get("fecha_inicio")
        contrato.fecha_fin = request.POST.get("fecha_fin")
        contrato.terminos = request.POST.get("terminos")
        contrato.monto = request.POST.get("monto")
        contrato.save()
        return redirect('gestion_contratos')  # O donde tengas la lista de contratos
    
    return JsonResponse({"error": "Método no permitido"}, status=405)
@login_required

def eliminar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id_contrato=contrato_id, id_usuario=request.user)
    if request.method == "POST":
        contrato.delete()
        return redirect('gestion_contratos')
    return JsonResponse({"error": "Método no permitido"}, status=405)

def editar_perfil(request):
    perfil = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # o a donde desees redirigir
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'perfil.html', {'form': form})


login_required
def seguimiento_tareas(request):
    """
    Muestra todas las tareas del usuario (por ejemplo, filtrando por proyecto).
    Ajusta el filtro según tu modelo: aquí asumo que el usuario es el dueño del proyecto.
    """
    # Filtra tareas cuyo proyecto pertenece al usuario
    tareas = Tarea.objects.filter(id_proyecto__id_usuario=request.user)
    return render(request, 'seguimiento_tareas.html', {'tareas': tareas})

@login_required
def iniciar_seguimiento(request, tarea_id):
    if request.method == 'POST':
        tarea = get_object_or_404(Tarea, id_tarea=tarea_id)
        now_time = timezone.now()
        seguimiento_activo = tarea.seguimientos.filter(fin__isnull=True).first()
        if seguimiento_activo:
            # Reinicia el seguimiento: actualiza la hora de inicio a la hora actual
            seguimiento_activo.inicio = now_time
            seguimiento_activo.save()
        else:
            # Crea un nuevo seguimiento con la hora actual
            seguimiento_activo = SeguimientoTiempo.objects.create(
                id_tarea=tarea,
                inicio=now_time
            )
        # Redirecciona a la vista de detalle de la tarea para que se muestre el cronómetro
        return redirect('detalle_tarea', id_tarea=tarea_id)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
"""    
@login_required
def iniciar_seguimiento(request, tarea_id):
    tarea = get_object_or_404(Tarea, id_tarea=tarea_id)
    # Si ya hay seguimiento activo para la tarea, no creamos otro
    seguimiento_activo = tarea.seguimientos.filter(fin__isnull=True).first()
    if not seguimiento_activo:
        SeguimientoTiempo.objects.create(
            id_tarea=tarea,
            inicio=timezone.now()
        )
        
        print("seguimineto iniciado")
    return redirect('seguimiento_tareas')
"""
@login_required
def detener_seguimiento(request, seguimiento_id):
    print("Detener seguimiento llamado con id_tiempo:", seguimiento_id) 
    seguimiento = get_object_or_404(SeguimientoTiempo, id_tiempo=seguimiento_id)
    if seguimiento.fin is None:
        print("Seguimiento activo, procediendo a detenerlo.")
        seguimiento.fin = timezone.now()
        diferencia = seguimiento.fin - seguimiento.inicio
        seguimiento.duracion = int(diferencia.total_seconds() // 60)
        seguimiento.save()
        print("Seguimiento detenido, duración guardada:", seguimiento.duracion)  
    else:
        print("El seguimiento ya estaba detenido.")
    return redirect('detalle_tarea', id_tarea=seguimiento.id_tarea.id_tarea)


@login_required
def resetear_seguimiento(request, tarea_id):
    """
    Si hay un seguimiento activo para la tarea, se resetea (se actualiza el tiempo de inicio a ahora).
    Si no existe, se crea uno nuevo.
    """
    tarea = get_object_or_404(Tarea, id_tarea=tarea_id)
    seguimiento = tarea.seguimientos.filter(fin__isnull=True).first()
    if seguimiento:
        seguimiento.inicio = timezone.now()
        seguimiento.save()
    else:
        SeguimientoTiempo.objects.create(
            id_tarea=tarea,
            inicio=timezone.now()
        )
    return redirect('seguimiento_tareas')




@login_required
def detalle_tarea(request, id_tarea):
    # Obtener la tarea
    tarea = get_object_or_404(Tarea, id_tarea=id_tarea)
    
    # Tiempo acumulado de seguimientos finalizados (en milisegundos)
    tiempo_acumulado = 0
    for seg in tarea.seguimientos.filter(fin__isnull=False):
        if seg.duracion is not None:
            # seg.duracion está en minutos, convertir a ms
            tiempo_acumulado += seg.duracion * 60 * 1000
        else:
            tiempo_acumulado += (seg.fin - seg.inicio).total_seconds() * 1000

    # Si hay un seguimiento activo, calcular el tiempo transcurrido (en ms)
    seguimiento_activo = tarea.seguimientos.filter(fin__isnull=True).first()
    if seguimiento_activo:
        tiempo_activo = (timezone.now() - seguimiento_activo.inicio).total_seconds() * 1000
    else:
        tiempo_activo = 0

    # Tiempo total al momento de renderizar (en ms)
    tiempo_total = int(tiempo_acumulado + tiempo_activo)
    
    return render(request, 'detalle_tarea.html', {
        'tarea': tarea,
        'seguimiento_activo': seguimiento_activo,
        'tiempo_total': tiempo_total,  # en ms
    })