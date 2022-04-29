from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from app import forms

from app.models import Archivos



class ArchivoListView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        archivos = Archivos.objects.all()
        context={
            'archivos': archivos,
            'titulo': 'Archivos'
        }
        return render(request, 'archivos/archivo_list.html', context)

class ArchivoCreateView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        notificaciones = Archivos.objects.all()
        context={
            'form':forms,
            'titulo': 'Crear Archivo'
        }
        return render(request, 'archivos/archivo_create.html', context)
