from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion.forms import UsuarioForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from .models import Proyecto
from django.views.decorators.csrf import csrf_exempt

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
    return render(request, 'perfil.html')


def registrar(request):
    form=UsuarioForm
    if request.method=='POST':
        print("Se recibió una solicitud POST")
        form= UsuarioForm(request.POST)
        if form.is_valid():
            print("El formulario es válido")
            form.save()
            user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            login(request,user)
            return redirect('inicio')
            #render(request,'index.html')
        else:
            print("El formulario no es válido")  # Muestra que hubo errores de validación
            print(form.errors)  # Muestra los errores específicos
    else:
        print("Se accedió al formulario con GET")
        form= UsuarioForm()
    return render(request,'registro.html', {'form':form })

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