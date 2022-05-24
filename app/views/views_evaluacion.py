from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
#from ..forms import EvaluacionCreateForm
from app import forms

from app.models import Evaluacion

class EvaluacionListView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        evaluacion = Evaluacion.objects.all()
        context={
            'evaluacion': evaluacion,
            'titulo': 'Evaluacion'
        }
        return render(request, 'evaluacion/evaluacion_list.html', context)

#class EvaluacionCreateView(LoginRequiredMixin ,View):
    
    #def get(self,request, *args, **kwargs):
        #form=EvaluacionCreateForm()
        #context={
            #'form': form,
            #'titulo': 'Crear Evaluacion'
        #}
        #return render(request, 'evaluacion/evaluacion_create.html', context)

