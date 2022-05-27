from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
from app.forms import PuntajeCreateForm


from app.models import Puntaje




#LISTAR PUNTAJE

class PuntajeListView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        puntaje = Puntaje.objects.all()
        context={
            'puntaje': puntaje,
            'titulo': 'Puntajes'
        }
        return render(request, 'puntaje/puntaje_list.html', context)

#CREAR PUNTAJE

class PuntajeCreateView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form=PuntajeCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Puntaje'
        }
        return render(request, 'puntaje/puntaje_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = PuntajeCreateForm(request.POST)
            if form.is_valid():
                clase = form.cleaned_data.get('clase')
                detalles = form.cleaned_data.get('detalles')
                
                u, created = Puntaje.objects.get_or_create(clase=clase,detalles=detalles)
                u.save()

                messages.success(request, "Puntaje agregado correctamente")
                return redirect('app:puntaje')

        
        context={
            'titulo': 'Crear Puntaje',
            'form': form
        }
        return render(request, 'puntaje/puntaje_create.html', context)