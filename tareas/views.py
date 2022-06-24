import re
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Usuario
from tareas.forms import ArchivoCreateForm, TareaCreateForm, ForoCreateForm, TareaEditForm
from django.contrib import messages

from tareas.models import Foro, Actividad, Puntaje, TipoForo, TipoActividad, UsuarioActividad

# Create your views here.

class TareasListView(LoginRequiredMixin, View):

    def get(self,request, tipo_id, *args, **kwargs):
        #CAMBIAR EL FILTRO POR EL QUE SE MANDE POR EL URL, PORQUE SERAN MUCHOS TIPOS QUE SE CREARAN DINAMICAMENTE
        actividades = Actividad.objects.filter(id_tipo_actividad=tipo_id)
        foros = Foro.objects.all()
        tipo = TipoActividad.objects.get(pk=tipo_id)

        #Obtiene la lista de foros para que en la plantilla html se pueda ver si existe una id de tarea
        list_foros = [foro.id_actividad for foro in foros]
        context={
            'list_foros': list_foros,
            'foros': foros,
            'actividades': actividades,
            'titulo': tipo.tipo,
            'tipo_act_nav': tipo.tipo,
            'tipo_id': tipo.id,
        }
        return render(request, 'tareas/tareas_list.html', context)



class TareasCreateView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form = TareaCreateForm(tipo_id=kwargs.get('tipo_id'))
        context={
            'form': form,
            'titulo': 'Crear Tarea',
            'tipo_id': kwargs.get('tipo_id'),
        }
        return render(request, 'tareas/tarea_create.html', context)

    def post(self, request, tipo_id, *args, **kwargs):
        if request.method=="POST":
            form = TareaCreateForm(tipo_id=kwargs.get('tipo_id'), data=request.POST)
            if form.is_valid():
                titulo = form.cleaned_data.get('titulo')
                fecha = form.cleaned_data.get('fecha')
                tipoTarea = TipoActividad.objects.get(pk=tipo_id)
                usuarioActual= request.user

                u, created = Actividad.objects.get_or_create(id_usuario=usuarioActual, titulo=titulo, id_tipo_actividad=tipoTarea , fecha=fecha)
                u.save()

                messages.success(request, "Tarea agregada correctamente")
                return redirect('tareas:tareas', tipo_id)

        
        context={
            'titulo': 'Crear Tarea',
            'form': form,
            'tipo_id': tipo_id
        }
        return render(request, 'tareas/tarea_create.html', context)


class TareaDetailsView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        tarea = get_object_or_404(Actividad, pk=pk)
        usuariosActividad = UsuarioActividad.objects.select_related('usuario','actividad','puntaje').filter(actividad_id=pk)
        puntajes = Puntaje.objects.filter(id_tipo_actividad=tarea.id_tipo_actividad)
        context={
            'puntajes': puntajes,
            'tarea': tarea,
            'usuarios':usuariosActividad,
            'titulo': 'Puntajes ' + tarea.titulo +" / Fecha: "+ str(tarea.fecha)
        }
        return render(request, 'tareas/tarea_details.html', context)

#Obtiene los usuario de la actividad
@csrf_exempt
def usuariosActividadAPI(request,pk):
    users = Usuario.objects.filter(id_tipo_usuario=3)

    data = []
    #Se verifica la existencia de cada usuario alumno en la tabla de usuario_actividad, y si no existe, se crea. Y todos se guardan en una lista
    for i in users:
        if not UsuarioActividad.objects.prefetch_related('usuario','actividad','puntaje').filter(actividad_id=pk,usuario_id=i.id).exists():
            UsuarioActividad.objects.create(actividad_id=pk,usuario_id=i.id)

        usuarioActividad = UsuarioActividad.objects.prefetch_related('usuario','actividad','puntaje').filter(actividad_id=pk,usuario_id=i.id)
        data.append(usuarioActividad)
    
    dataList = []
    tarea = get_object_or_404(Actividad, pk=pk)
    puntajes = list(Puntaje.objects.filter(id_tipo_actividad=tarea.id_tipo_actividad).values())
    for i in data:
        idUser = i.values('usuario').get()['usuario']
        idPuntaje = i.values('puntaje').get()['puntaje']
        usuario = Usuario.objects.get(pk=idUser)
        try:
            puntaje = Puntaje.objects.get(pk=idPuntaje)
            puntajeP = puntaje.puntaje
        except ObjectDoesNotExist:
            puntajeP = None
        
        nombre = usuario.nombre
        apellido_paterno = usuario.apellido_paterno
        apellido_materno = usuario.apellido_materno

        dataList.append({'id':idUser,'nombre':nombre, 'apellido_paterno':apellido_paterno, 'apellido_materno':apellido_materno,
                        'puntajeID':idPuntaje, 'puntaje':puntajeP, 'opcionesPuntaje':puntajes})
    return JsonResponse(dataList, safe=False)

#Actualiza el puntaje de la actividad
@csrf_exempt
def updatePuntaje(request):
    userID = request.POST.get('usuario')
    puntajeID = request.POST.get('puntaje')
    #puntajeObject = get_object_or_404(Puntaje, pk=puntajeID)
    actividadID = request.POST.get('actividad')

    if puntajeID == '0':
        puntajeID = None

    if UsuarioActividad.objects.filter(usuario=userID, actividad=actividadID).exists():
        UsuarioActividad.objects.filter(usuario=userID, actividad=actividadID).update(puntaje=puntajeID)
    else:
        usuarioActividad = UsuarioActividad.objects.get_or_create(usuario=userID, actividad=actividadID)
        usuarioActividad.puntaje = puntajeID
        usuarioActividad.save()

    return JsonResponse('Puntaje actualizado', safe=False)


class TareaDeleteView(LoginRequiredMixin, DeleteView):
    model = Actividad
    success_url = reverse_lazy('tareas:tareas')

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Eliminado correctamente")
        print(self.object.id_tipo_actividad.id)
        tipo_id = self.object.id_tipo_actividad.id
        return reverse('tareas:tareas', kwargs={'tipo_id': tipo_id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class TareaEditView(LoginRequiredMixin, UpdateView):
    model = Actividad
    form_class = TareaEditForm
    template_name = "tareas/tarea_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar tarea'
        context['tipo_id'] = self.object.id_tipo_actividad.id
        return context
    
    #def get_form_kwargs(self, *args, **kwargs):
    #    print(self.object.id_tipo_actividad.id)
    #    tipo_id = self.object.id_tipo_actividad.id
    #    print("aaaa"+ str(tipo_id))
    #    kwargs.update({'tipo_id': tipo_id})
    #    return kwargs

    def get_success_url(self):
        messages.success(self.request, "La tarea ha sido actualizada correctamente")
        print(self.object.id_tipo_actividad.id)
        tipo_id = self.object.id_tipo_actividad.id
        return reverse('tareas:tareas', kwargs={'tipo_id': tipo_id})


class ForosListView(LoginRequiredMixin, View):

    def get(self,request, *args, **kwargs):
        foros = Foro.objects.all()

        context={
            'foros': foros,
            'titulo': 'Foros'
        }
        return render(request, 'foro/foros_list.html', context)


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
                tarea = form.cleaned_data.get('id_actividad')

                u, created = Foro.objects.get_or_create(titulo=titulo, descripcion=descripcion , id_tipo_foro=tipoForo, id_actividad=tarea)
                u.save()

                messages.success(request, "Foro agregado correctamente")
                return redirect('tareas:foros')

        
        context={
            'titulo': 'Crear foro',
            'form': form
        }
        return render(request, 'tareas/tarea_create.html', context)


class ForoEditView(LoginRequiredMixin, UpdateView):
    model = Foro
    form_class = ForoCreateForm
    template_name = "foro/foro_edit.html"


    def get_success_url(self):
        messages.success(self.request, "El foro ha sido actualizado correctamente")
        return reverse_lazy('tareas:foros')


#Se muestra el foro seleccionado, las preguntas y respuestas
class ForoDetailsView(LoginRequiredMixin, View):
    
    def get(self,request, pk, *args, **kwargs):
        foro = get_object_or_404(Foro, pk=pk)
        context={
            'foro': foro,
            'descripcion': foro.descripcion,
            'titulo': 'Foro '
        }
        return render(request, 'foro/foro_details.html', context)

class ForoDeleteView(LoginRequiredMixin, DeleteView):
    model = Foro
    success_url = reverse_lazy('tareas:foros')

    def get_success_url(self):
        messages.success(self.request, "Eliminado correctamente")
        return reverse('tareas:foros')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class CajaDePreguntasListView(LoginRequiredMixin, View):

    def get(self,request, *args, **kwargs):
        tareas_caja = Actividad.objects.filter(id_tipo_actividad=2)

        context={
            'tareas_caja': tareas_caja,
            'titulo': 'Caja de preguntas'
        }
        return render(request, 'caja_preguntas/caja_preguntas_list.html', context)

class CajaDePreguntasCreateView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form = TareaCreateForm()
        context={
            'form': form,
            'titulo': 'Crear registro de Caja de Preguntas'
        }
        return render(request, 'caja_preguntas/caja_preguntas_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = CajaDePreguntasCreateForm(request.POST)
            if form.is_valid():
                fecha = form.cleaned_data.get('fecha')
                tipoTarea = TipoActividad.objects.get(pk=2)
                usuarioActual= request.user

                u, created = Actividad.objects.get_or_create(id_usuario=usuarioActual, id_tipo_actividad=tipoTarea , fecha=fecha)
                u.save()

                messages.success(request, "Tarea agregada correctamente")
                return redirect('tareas:caja_preguntas_list')

        
        context={
            'titulo': 'Crear registro de Caja de Preguntas',
            'form': form
        }
        return render(request, 'caja_preguntas/caja_preguntas_create.html', context)

class CajaDePreguntasDeleteView(LoginRequiredMixin, DeleteView):
    model = Actividad
    success_url = reverse_lazy('tareas:caja_preguntas_list')

    def get_success_url(self):
        messages.success(self.request, "Eliminado correctamente")
        return reverse('tareas:caja_preguntas_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)