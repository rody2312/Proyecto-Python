from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView, UpdateView
from ..forms import NotificacionCreateForm
from app import forms
from django.contrib import messages
from app.mixins import AdminUserMixin, ProfesorUserMixin

from app.models import Notificacion

#LISTAR NOTIFICACION

class NotificacionListView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin ,View):
     
    def get(self,request, *args, **kwargs):

        notificaciones = Notificacion.objects.all()
        context={
            'notificaciones': notificaciones,
            'titulo': 'Notificaciones'
        }
        return render(request, 'notificacion/notificacion_list.html', context)

#CREAR NOTIFICACION

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
                descripcion = form.cleaned_data.get('texto')
                usuarioActual= request.user

                u, created = Notificacion.objects.get_or_create(texto=descripcion, id_usuario=usuarioActual)
                u.save()

                messages.success(request, "Notificacion agregada correctamente")
                return redirect('app:notificacion')
        context={
            'titulo': 'Crear Notificacion',
            'form': form
        }
        return render(request, 'notificacion/notificacion_create.html', context)

#ELIMINAR NOTIFICACION

class NotificacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Notificacion
    success_url = reverse_lazy('app:notificacion')

    def get_success_url(self):
        messages.success(self.request, "Eliminado correctamente")
        return reverse('app:notificacion')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

#EDITAR NOTIFICACION

class NotificacionEditView(LoginRequiredMixin, UpdateView):
    model = Notificacion
    form_class = forms.NotificacionCreateForm
    template_name = "notificacion/notificacion_edit.html"

    def get_success_url(self):
        messages.success(self.request, "La notificacion ha sido actualizado correctamente")
        return reverse_lazy('app:notificacion')
