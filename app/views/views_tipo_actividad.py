from http.client import error
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView, UpdateView
from app.mixins import AdminUserMixin, ProfesorUserMixin

from tareas.models import Actividad, Puntaje, TipoActividad, UsuarioActividad
from app import forms
from django.contrib import messages

# LISTAR TIPO ACTIVIDAD

class TipoActividadListView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin ,View):
     
    def get(self,request, *args, **kwargs):

        tipo_actividad = TipoActividad.objects.all()
        context={
            'tipo_actividades': tipo_actividad,
            'titulo': 'Tipos de Actividades'
        }
        return render(request, 'actividad/tipo_actividad_list.html', context)

#CREAR TIPO ACTIVIDAD

class TipoActividadCreateView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin ,View):
    
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
# NO USAR ########################
class TipoActividadDeleteView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin, DeleteView):
    model = TipoActividad
    success_url = reverse_lazy('app:list_tipo_actividad')
    #
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if Actividad.objects.filter(id_tipo_actividad=self.object.id).exists():
            print('a')
            messages.success(self.request, "No se puede eliminar el usuario")
            return HttpResponseForbidden('xD')
        else:
            print('b')
            messages.success(self.request, "A")
            success_url = self.get_success_url()
            #self.object.delete()
            return HttpResponseRedirect(success_url)

#SI USAR
def delete(request, pk, *args, **kwargs):
    tipo = TipoActividad.objects.get(id=pk)
    if Actividad.objects.filter(id_tipo_actividad=pk).exists():
        messages.error(request, "No se puede eliminar, debido a que existen registros de actividades relacionados a '" + tipo.tipo +"'")
        return HttpResponseRedirect(reverse_lazy('app:list_tipo_actividad'))
    else:
        if tipo.delete():
            messages.success(request, "Se elimino correctamente")
        return HttpResponseRedirect(reverse_lazy('app:list_tipo_actividad'))

#EDITAR TIPO ACTIVIDAD

class TipoActividadEditView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin, UpdateView):
    model = TipoActividad
    form_class = forms.TipoActividadCreateForm
    template_name = "actividad/tipo_actividad_edit.html"

    def get_success_url(self):
        messages.success(self.request, "El tipo de actividad ha sido actualizado correctamente")
        return reverse_lazy('app:list_tipo_actividad')


class TipoActividadDetailsView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin , View):
    def get(self, request, pk, *args, **kwargs):
        tipoActividad = get_object_or_404(TipoActividad, pk=pk)
        puntajes = Puntaje.objects.filter(id_tipo_actividad=pk)
        context={
            'puntajes':puntajes,
            'tipoActividad':tipoActividad,
            'tipo_id':pk,
            'titulo':'Puntajes',
        }
        return render(request, 'actividad/tipo_actividad_puntajes.html', context)

#Eliminar tipo de asistencia SI USAR##
def deletePuntaje(request, pk, *args, **kwargs):
    puntaje = Puntaje.objects.get(id=pk)

    #Comprobar si el puntaje existe en algun registro de actividad
    if UsuarioActividad.objects.filter(puntaje=pk).exists():
        messages.error(request, "No se puede eliminar, debido a que existen registros de puntaje relacionados a '" + str(puntaje.puntaje) + "'")
        return HttpResponseRedirect(reverse_lazy('app:tipo_actividad_puntajes', kwargs={'pk': puntaje.id_tipo_actividad.id}))
    else:
        if puntaje.delete():
            messages.success(request, "Se elimino correctamente")
        return HttpResponseRedirect(reverse_lazy('app:tipo_actividad_puntajes', kwargs={'pk': puntaje.id_tipo_actividad.id}))

#Views para crear y editar un puntaje a un tipo de asistencia

class PuntajeCreateView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form=forms.PuntajeCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Nuevo Puntaje',
        }
        return render(request, 'actividad/puntaje_create.html', context)

    def post(self, request, tipo_id, *args, **kwargs):
        if request.method=="POST":
            form = forms.PuntajeCreateForm(request.POST)
            if form.is_valid():
                puntaje = form.cleaned_data.get('puntaje')

                u, created = Puntaje.objects.get_or_create(puntaje=puntaje, id_tipo_actividad=TipoActividad.objects.get(id=tipo_id))
                u.save()

                messages.success(request, "Puntaje agregado correctamente")
                return redirect('app:tipo_actividad_puntajes', tipo_id)
        context={
            'titulo': 'Crear nuevo puntaje',
            'form': form
        }
        return render(request, 'actividad/puntaje_create.html', context)



class PuntajeEditView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin, UpdateView):
    model = Puntaje
    form_class = forms.PuntajeCreateForm
    template_name = "actividad/puntaje_create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar puntaje'
        return context

    def get_success_url(self):
        messages.success(self.request, "El puntaje ha sido actualizado correctamente")
        return reverse_lazy('app:tipo_actividad_puntajes', kwargs={'pk': self.kwargs['tipo_id']})