from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View
from ..forms import NotificacionCreateForm
from app import forms
from django.contrib import messages

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

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = NotificacionCreateForm(request.POST)
            if form.is_valid():
                descripcion = form.cleaned_data.get('descripcion')
                alumno = form.cleaned_data.get('alumno')
                fecha = form.cleaned_data.get('fecha')

                u, created = Notificacion.objects.get_or_create(descripcion=descripcion,alumno=alumno,fecha=fecha,)
                u.save()

                messages.success(request, "Notificacion agregada correctamente")
                return redirect('app:notificacion')
