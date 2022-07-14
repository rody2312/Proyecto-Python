from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView, UpdateView
from app.models import Usuario
from evaluacion.forms import EvaluacionCreateForm, PuntajeEvCreateForm
from app import forms
from django.contrib import messages
from evaluacion.models import Evaluacion, PuntajeEvaluacion, UsuarioEvaluacion
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from app.mixins import AdminProfesorUserMixin, AdminUserMixin, ProfesorUserMixin
from tareas.models import Actividad



#LISTAR EVALUACION

class EvaluacionListView(LoginRequiredMixin, AdminProfesorUserMixin ,View):
    
    def get(self,request, *args, **kwargs):
        evaluaciones = Evaluacion.objects.all()
        context={
            'evaluaciones': evaluaciones,
            'titulo': 'Evaluaciones'
        }
        return render(request, 'evaluacion/evaluacion_list.html', context)

#CREAR EVALUACION

class EvaluacionCreateView(LoginRequiredMixin, AdminProfesorUserMixin ,View):
    def get(self,request, *args, **kwargs):
        form=EvaluacionCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Evaluación'
        }
        return render(request, 'evaluacion/evaluacion_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = EvaluacionCreateForm(request.POST)
            if form.is_valid():
                titulo = form.cleaned_data.get('titulo')
                fecha = form.cleaned_data.get('fecha')
                usuarioActual= request.user
                
                if not Actividad.objects.filter(fecha=fecha).exists():
                    u, created = Evaluacion.objects.get_or_create(id_usuario=usuarioActual, titulo=titulo, fecha=fecha)
                    u.save()
                    messages.success(request, "Evaluacion agregada correctamente")
                else:
                    messages.error(request, "Ya existe un registro de actividad en la fecha " + str(fecha))
                return redirect('evaluacion:evaluaciones')

        context={
            'titulo': 'Crear Evaluación',
            'form': form
        }
        return render(request, 'evaluacion/evaluacion_create.html', context)

# ELIMINAR EVALUACION                

class EvaluacionDeleteView(LoginRequiredMixin, AdminProfesorUserMixin, DeleteView):
    model = Evaluacion
    success_url = reverse_lazy('evaluacion:evaluaciones')

    def get_success_url(self):
        messages.success(self.request, "Eliminada correctamente")
        return reverse('evaluacion:evaluaciones')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

# DETALLES EVALUACION

class EvaluacionDetailsView(LoginRequiredMixin, AdminProfesorUserMixin, View):
    def get(self, request, pk, *args, **kwargs):
        evaluacion = get_object_or_404(Evaluacion, pk=pk)
        context={
            'evaluacion': evaluacion,
            'titulo': 'Evaluación ' + evaluacion.titulo +" / Fecha: "+ str(evaluacion.fecha)
        }
        return render(request, 'evaluacion/evaluacion_details.html', context)

class EvaluacionEditView(LoginRequiredMixin, AdminProfesorUserMixin, UpdateView):
    model = Evaluacion
    form_class = EvaluacionCreateForm
    template_name = "evaluacion/evaluacion_create.html"

    def get_success_url(self):
        messages.success(self.request, "La evaluación ha sido actualizado correctamente")
        return reverse_lazy('evaluacion:evaluaciones')


#Obtiene los usuario de la evaluación
@csrf_exempt
def usuariosEvaluacionAPI(request,pk):
    users = Usuario.objects.filter(id_tipo_usuario=3)

    data = []
    #Se verifica la existencia de cada usuario alumno en la tabla de usuario_evaluacion, y si no existe, se crea. Y todos se guardan en una lista
    for i in users:
        if not UsuarioEvaluacion.objects.prefetch_related('usuario','evaluacion','puntaje').filter(evaluacion_id=pk,usuario_id=i.id).exists():
            UsuarioEvaluacion.objects.create(evaluacion_id=pk,usuario_id=i.id)

        usuarioEvaluacion = UsuarioEvaluacion.objects.prefetch_related('usuario',' evaluacion','puntaje').filter(evaluacion_id=pk,usuario_id=i.id)
        data.append(usuarioEvaluacion)
    
    dataList = []
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    puntajes = list(PuntajeEvaluacion.objects.all().values())
    for i in data:
        idUser = i.values('usuario').get()['usuario']
        idPuntaje = i.values('puntaje').get()['puntaje']
        usuario = Usuario.objects.get(pk=idUser)
        try:
            puntaje = PuntajeEvaluacion.objects.get(pk=idPuntaje)
            puntajeP = puntaje.puntaje
        except ObjectDoesNotExist:
            puntajeP = None
        
        nombre = usuario.nombre
        apellido_paterno = usuario.apellido_paterno
        apellido_materno = usuario.apellido_materno

        dataList.append({'id':idUser,'nombre':nombre, 'apellido_paterno':apellido_paterno, 'apellido_materno':apellido_materno,
                        'puntajeID':idPuntaje, 'puntaje':puntajeP, 'opcionesPuntaje':puntajes})
    return JsonResponse(dataList, safe=False)


#Actualiza el puntaje de la evaluación
@csrf_exempt
def updatePuntaje(request):
    userID = request.POST.get('usuario')
    puntajeID = request.POST.get('puntaje')
    #puntajeObject = get_object_or_404(Puntaje, pk=puntajeID)
    evaluacionID = request.POST.get('evaluacion')

    if puntajeID == '0':
        puntajeID = None

    if UsuarioEvaluacion.objects.filter(usuario=userID, evaluacion=evaluacionID).exists():
        UsuarioEvaluacion.objects.filter(usuario=userID, evaluacion=evaluacionID).update(puntaje=puntajeID)
    else:
        usuarioEvaluacion = UsuarioEvaluacion.objects.get_or_create(usuario=userID, evaluacion=evaluacionID)
        usuarioEvaluacion.puntaje = puntajeID
        usuarioEvaluacion.save()

    return JsonResponse('Puntaje actualizado', safe=False)



#### Views CRUD Puntaje Evaluacion #####

#Mostrar todos los puntajes de evaluación
class PuntajesEvListView(LoginRequiredMixin, AdminUserMixin, View):
    def get(self, request, *args, **kwargs):
        puntajes = PuntajeEvaluacion.objects.all()
        context={
            'puntajes':puntajes,
            'titulo':'Puntajes de evaluacion',
        }
        return render(request, 'evaluacion/puntajes_ev_list.html', context)

#Eliminar puntaje de evaluacion
def deletePuntajeEv(request, pk, *args, **kwargs):
    puntajeEv = PuntajeEvaluacion.objects.get(id=pk)

    #Comprobar si el puntaje existe en algun registro de actividad
    if UsuarioEvaluacion.objects.filter(puntaje=pk).exists():
        messages.error(request, "No se puede eliminar, debido a que existen registros de puntaje relacionados a '" + str(puntajeEv.puntaje) + "'")
        return HttpResponseRedirect(reverse_lazy('evaluacion:evaluacion_puntajes'))
    else:
        if puntajeEv.delete():
            messages.success(request, "Se elimino correctamente")
        return HttpResponseRedirect(reverse_lazy('evaluacion:evaluacion_puntajes'))

#Views para crear y editar un puntaje a un tipo de asistencia

class PuntajeEvCreateView(LoginRequiredMixin, AdminUserMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form=forms.PuntajeCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Nuevo Puntaje',
        }
        return render(request, 'evaluacion/puntajes_ev_create.html', context)

    def post(self, request, *args, **kwargs):
        if request.method=="POST":
            form = PuntajeEvCreateForm(request.POST)
            if form.is_valid():
                puntaje = form.cleaned_data.get('puntaje')

                u, created = PuntajeEvaluacion.objects.get_or_create(puntaje=puntaje)
                u.save()

                messages.success(request, "Puntaje agregado correctamente")
                return redirect('evaluacion:evaluacion_puntajes')
        context={
            'titulo': 'Crear nuevo puntaje',
            'form': form
        }
        return render(request, 'evaluacion/puntajes_ev_create.html', context)



class PuntajeEvEditView(LoginRequiredMixin, AdminUserMixin, UpdateView):
    model = PuntajeEvaluacion
    form_class = PuntajeEvCreateForm
    template_name = "evaluacion/puntajes_ev_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar puntaje'
        return context

    def get_success_url(self):
        messages.success(self.request, "El puntaje ha sido actualizado correctamente")
        return reverse_lazy('evaluacion:evaluacion_puntajes')
