from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from ..forms import NotificacionCreateForm
from app import forms

from app.models import Notificacion


class NotificacionListView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):

        notificaciones = Notificacion.objects.all()
        context={
            'notificaciones': notificaciones,
            'titulo': 'Notificaciones'
        }
        return render(request, 'notificacion/notificacion_list.html', context)

class NotificacionCreateView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form=NotificacionCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Notificacion'
        }
        return render(request, 'notificacion/notificacion_create.html', context)

