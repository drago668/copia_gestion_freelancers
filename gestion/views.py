from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion.forms import UsuarioForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from .models import Proyecto,Contrato
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomAuthenticationForm

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
        #monto_acordado = request.POST.get("monto")  # Campo corregido

        if nombre_cliente and fecha_inicio and fecha_fin:
            Contrato.objects.create(
                id_usuario=request.user,
                nombre_cliente=nombre_cliente,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
               # monto_acordado=monto_acordado
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