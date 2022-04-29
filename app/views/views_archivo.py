from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from app import forms
from tareas.forms import ArchivoCreateForm
from tareas.models import Archivo




class ArchivoListView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        archivos = Archivo.objects.all()
        context={
            'archivos': archivos,
            'titulo': 'Archivos'
        }
        return render(request, 'archivos/archivo_list.html', context)

class ArchivoCreateView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form = ArchivoCreateForm()
        notificaciones = Archivo.objects.all()
        context={
            'form': form,
            'titulo': 'Crear Archivo'
        }
        return render(request, 'archivos/archivo_create.html', context)
