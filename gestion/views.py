from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestion.forms import UsuarioForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login

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