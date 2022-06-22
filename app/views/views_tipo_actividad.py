from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView, UpdateView

from tareas.models import TipoActividad
from app import forms
from django.contrib import messages

# LISTAR TIPO ACTIVIDAD

class TipoActividadListView(LoginRequiredMixin ,View):
     
    def get(self,request, *args, **kwargs):

        tipo_actividad = TipoActividad.objects.all()
        context={
            'tipo_actividades': tipo_actividad,
            'titulo': 'Tipo actividad'
        }
        return render(request, 'actividad/tipo_actividad_list.html', context)

#CREAR TIPO ACTIVIDAD

class TipoActividadCreateView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form=forms.TipoActividadCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Tipo de Actividad'
        }
        return render(request, 'actividad/tipo_actividad_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = forms.TipoActividadCreateForm(request.POST)
            if form.is_valid():
                nombre_tipo = form.cleaned_data.get('tipo')

                u, created = TipoActividad.objects.get_or_create(tipo=nombre_tipo)
                u.save()

                messages.success(request, "Tipo de actividad agregada correctamente")
                return redirect('app:list_tipo_actividad')
        context={
            'titulo': 'Crear tipo actividad',
            'form': form
        }
        return render(request, 'actividad/tipo_actividad_create.html', context)

#ELIMINAR TIPO ACTIVIDAD

class TipoActividadDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoActividad
    success_url = reverse_lazy('app:list_tipo_actividad')

    def get_success_url(self):
        messages.success(self.request, "Eliminado correctamente")
        return reverse('app:list_tipo_actividad')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

#EDITAR TIPO ACTIVIDAD

class TipoActividadEditView(LoginRequiredMixin, UpdateView):
    model = TipoActividad
    form_class = forms.TipoActividadCreateForm
    template_name = "actividad/tipo_actividad_edit.html"

    def get_success_url(self):
        messages.success(self.request, "El tipo de actividad ha sido actualizado correctamente")
        return reverse_lazy('app:list_tipo_actividad')