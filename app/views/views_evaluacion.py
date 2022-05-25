from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView
from ..forms import EvaluacionCreateForm
from app import forms
from django.contrib import messages

from app.models import Evaluacion


#LISTAR EVALUACION

class EvaluacionListView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        evaluaciones = Evaluacion.objects.all()
        context={
            'evaluaciones': evaluaciones,
            'titulo': 'Evaluaciones'
        }
        return render(request, 'evaluacion/evaluacion_list.html', context)

#CREAR EVALUACION

class EvaluacionCreateView(LoginRequiredMixin ,View):
    def get(self,request, *args, **kwargs):
        form=EvaluacionCreateForm
        context={
            'form': form,
            'titulo': 'Crear Evaluacion'
        }
        return render(request, 'evaluacion/evaluacion_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = EvaluacionCreateForm(request.POST)
            if form.is_valid():
                titulo = form.cleaned_data.get('titulo')
                descripcion = form.cleaned_data.get('descripcion')
                fecha = form.cleaned_data.get('fecha')
                
                u, created = Evaluacion.objects.get_or_create(titulo=titulo, descripcion=descripcion, fecha=fecha)
                u.save()

                messages.success(request, "Evaluacion agregada correctamente")
                return redirect('app:evaluacion')


# ELIMINAR EVALUACION                

class EvaluacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Evaluacion
    success_url = reverse_lazy('app:evaluacion_delete')

    def get_success_url(self):
        messages.success(self.request, "Eliminada correctamente")
        return reverse('app:evaluacion_delete')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)











#class EvaluacionDetailsView(LoginRequiredMixin ,View):
    #def get(self, request, pk, *args, **kwargs):
        #usuario = get_object_or_404(Usuario, pk=pk)
        #context={
            #'usuario':usuario
        #}
       # return render(request, 'evaluacion/evaluacion_details.html', context)


