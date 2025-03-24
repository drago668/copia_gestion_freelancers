from django.shortcuts import render
from django.http import HttpResponse


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