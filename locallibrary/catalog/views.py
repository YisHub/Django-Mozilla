from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def mi_vista(request):
    # Lógica de la vista
    return HttpResponse("Hola, mundo!")