from django.shortcuts import render
from app.mixins import AdminUserMixin, ProfesorUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from foro.forms import ForoCreateForm
from foro.models import Foro
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect


# Create your views here.


class ForosListView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin, View):

    def get(self,request, *args, **kwargs):
        foros = Foro.objects.all()

        context={
            'foros': foros,
            'titulo': 'Foros'
        }
        return render(request, 'foro/foros_list.html', context)


class ForoCreateView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin, View):
    
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
                tarea = form.cleaned_data.get('id_actividad')

                u, created = Foro.objects.get_or_create(titulo=titulo, descripcion=descripcion , id_tipo_foro=tipoForo, id_actividad=tarea)
                u.save()

                messages.success(request, "Foro agregado correctamente")
                return redirect('foro:foros')

        
        context={
            'titulo': 'Crear foro',
            'form': form
        }
        return render(request, 'tareas/tarea_create.html', context)


class ForoEditView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin, UpdateView):
    model = Foro
    form_class = ForoCreateForm
    template_name = "foro/foro_edit.html"


    def get_success_url(self):
        messages.success(self.request, "El foro ha sido actualizado correctamente")
        return reverse_lazy('foro:foros')


#Se muestra el foro seleccionado, las preguntas y respuestas
class ForoDetailsView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin, View):
    
    def get(self,request, pk, *args, **kwargs):
        foro = get_object_or_404(Foro, pk=pk)
        context={
            'foro': foro,
            'descripcion': foro.descripcion,
            'titulo': 'Foro '
        }
        return render(request, 'foro/foro_details.html', context)

class ForoDeleteView(LoginRequiredMixin, AdminUserMixin, ProfesorUserMixin, DeleteView):
    model = Foro
    success_url = reverse_lazy('foro:foros')

    def get_success_url(self):
        messages.success(self.request, "Eliminado correctamente")
        return reverse('foro:foros')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)