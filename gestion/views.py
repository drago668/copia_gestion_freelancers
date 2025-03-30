from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion.forms import UsuarioForm
from django.contrib.auth import logout


def index(request):
    return render(request, 'index.html')

def contrato(request): #aqui se configuran la logica para visulaizar los contratos
    return render(request,'contrato.html')
def proyecto(request):
    return render(request, 'proyecto.html')
def tiempo(request):
    return render(request,'tiempo.html')
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