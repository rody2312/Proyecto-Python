from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Usuario
from tareas.forms import ArchivoCreateForm, TareaCreateForm, ForoCreateForm
from django.contrib import messages

from tareas.models import Foro, Tarea, TipoForo, TipoTarea

# Create your views here.

class TareasListView(LoginRequiredMixin, View):

    def get(self,request, *args, **kwargs):
        tareas = Tarea.objects.all()
        foros = Foro.objects.all()

        #Obtiene la lista de foros para que en la plantilla html se pueda ver si existe una id de tarea
        list_foros = [foro.id for foro in foros]
        context={
            'list_foros': list_foros,
            'tareas': tareas,
            'titulo': 'Tareas'
        }
        return render(request, 'tareas/tareas_list.html', context)



class TareasCreateView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form = TareaCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Tarea'
        }
        return render(request, 'tareas/tarea_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = TareaCreateForm(request.POST)
            if form.is_valid():
                fecha = form.cleaned_data.get('fecha')
                tipoTarea = TipoTarea.objects.get(pk=1)
                usuarioActual= request.user

                u, created = Tarea.objects.get_or_create(id_usuario=usuarioActual, id_tipo_tarea=tipoTarea , fecha=fecha)
                u.save()

                messages.success(request, "Tarea agregada correctamente")
                return redirect('tareas:tareas')

        
        context={
            'titulo': 'Crear Usuario',
            'form': form
        }
        return render(request, 'tareas/tarea_create.html', context)


class TareaDetailsView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        usuarios = Usuario.objects.all()
        tarea = get_object_or_404(Tarea, pk=pk)
        context={
            'usuarios':usuarios,
            'titulo': 'Detalles ' + tarea.titulo +" / Fecha: "+ str(tarea.fecha)
        }
        return render(request, 'tareas/tarea_details.html', context)


class TareaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarea
    success_url = reverse_lazy('tareas:tareas')

    def get_success_url(self):
        messages.success(self.request, "Eliminado correctamente")
        return reverse('tareas:tareas')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class TareaEditView(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaCreateForm
    template_name = "tareas/tarea_edit.html"

    def get_success_url(self):
        messages.success(self.request, "La tarea ha sido actualizado correctamente")
        return reverse_lazy('tareas:tareas')


class ForoCreateView(LoginRequiredMixin, View):
    
    def get(self,request, *args, **kwargs):
        form = ForoCreateForm()
        context={
            'form': form,
            'titulo': 'Crear foro'
        }
        return render(request, 'foro/foro_create.html', context)
    
    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = ForoCreateForm(request.POST)
            if form.is_valid():
                titulo = form.cleaned_data.get('titulo')
                descripcion = form.cleaned_data.get('descripcion')
                tipoForo = form.cleaned_data.get('id_tipo_foro')
                tarea = Tarea.objects.get(pk=self.kwargs['pk'])
                

                u, created = Foro.objects.get_or_create(titulo=titulo, descripcion=descripcion , id_tipo_foro=tipoForo, id_tarea=tarea)
                u.save()

                messages.success(request, "Tarea agregada correctamente")
                return redirect('tareas:tareas')

        
        context={
            'titulo': 'Crear foro',
            'form': form
        }
        return render(request, 'tareas/tarea_create.html', context)