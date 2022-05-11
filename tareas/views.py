from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from tareas.forms import ArchivoCreateForm, TareaCreateForm
from django.contrib import messages

from tareas.models import Tarea

# Create your views here.

class TareasListView(LoginRequiredMixin, View):

    def get(self,request, *args, **kwargs):
        tareas = Tarea.objects.all()
        context={
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
                titulo = form.cleaned_data.get('titulo')
                fecha = form.cleaned_data.get('fecha')
                descripcion = form.cleaned_data.get('descripcion')
                usuarioActual= request.user
                print(usuarioActual)

                u, created = Tarea.objects.get_or_create(id_usuario=usuarioActual, titulo=titulo, fecha=fecha, descripcion=descripcion)
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
        usuario = get_object_or_404(Tarea, pk=pk)
        context={
            'usuario':usuario
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
