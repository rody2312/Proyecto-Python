import re
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Usuario
from asistencia.models import Asistencia, UsuarioAsistencia
from evaluacion.models import Evaluacion, UsuarioEvaluacion
from tareas.forms import TareaCreateForm, ForoCreateForm, TareaEditForm
from django.contrib import messages

from tareas.models import Foro, Actividad, Puntaje, TipoForo, TipoActividad, UsuarioActividad

# Create your views here.

class TareasListView(LoginRequiredMixin, View):

    def get(self,request, tipo_id, *args, **kwargs):
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
    ### La razon de hacer esto es para que se actualice siempre la lista, en caso de que se cree un usuario, se vuelva a actualizar #####
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


class ResumenListView(LoginRequiredMixin, View):

    def get(self,request, *args, **kwargs):
        actividades = Actividad.objects.all()
        evaluaciones = Evaluacion.objects.all()
        asistencias = Asistencia.objects.all()
        fechas = []
        for (a,b,c) in zip(actividades,evaluaciones,asistencias):
            if a.fecha not in fechas: fechas.append(a.fecha)
            if b.fecha not in fechas: fechas.append(b.fecha)
            if c.fecha not in fechas: fechas.append(c.fecha)
        
        #Ordenar lista de fechas de forma descendiente
        fechas.sort(reverse=True)
        context={
            'fechas': fechas,
            'titulo': 'Resumen'
        }
        return render(request, 'puntajes/puntajes_list.html', context)


class ResumenDetailsView(LoginRequiredMixin, View):

    def get(self, request, fecha, *args, **kwargs):
        #columnas para listar en el template
        columnas = []
        #alumnos para listar en el template
        alumnos = []
        alumnosList = []
        alumnosListEv = []
        #Obtiene todos los usuarios alumno
        alumnos = Usuario.objects.filter(id_tipo_usuario=3)


        if Evaluacion.objects.filter(fecha=fecha).exists():
            columnas.append('Evaluación')
            
            for a in alumnos:
                alumno=[]
                alumno.append(a.nombre)
                alumno.append(a.apellido_paterno)
                alumno.append(a.apellido_materno)

                puntajeEv = UsuarioEvaluacion.objects.filter(usuario_id=a.id,evaluacion__fecha=fecha)

                if puntajeEv:
                    alumno.append(puntajeEv.values('puntaje_id__puntaje')[0]['puntaje_id__puntaje'])
                else:
                    alumno.append('0')
                
                alumnosListEv.append(alumno)

        else:
            tipoActividades = TipoActividad.objects.all()
            columnas.append('Asistencia')
            for x in tipoActividades:
                columnas.append(x.tipo)

            #Se itera cada alumno para ir agregando 1 por 1 a la lista de alumnos que se mostrara en el template
            for a in alumnos:
                alumno=[]
                alumno.append(a.nombre)
                alumno.append(a.apellido_paterno)
                alumno.append(a.apellido_materno)
                #Obtiene el puntaje de asistencia del alumno actual, y lo agrega a la variable
                alumno.append(UsuarioAsistencia.objects.filter(usuario_id=a.id,asistencia__fecha=fecha).values('tipo_asistencia__puntaje')[0]['tipo_asistencia__puntaje'])
                
                #Crear lista de puntajes de todas las actividades
                puntajeList= []

                puntajes = TipoActividad.objects.filter(actividades_tipos__usuarioactividad__usuario_id=a.id,actividades_tipos__fecha=fecha).values(
                    'tipo','actividades_tipos__usuarioactividad__puntaje_id__puntaje').order_by('id')
                print(puntajes)

                #Se verifica si la query de obtener los puntajes del usuario existe al menos un puntaje, y en caso de que no exista, se agregan 0
                if puntajes:
                    cont=0
                    for t in range(tipoActividades.count()):
                        try:
                            #Si encuentra un dato en ese index (t), entonces se agrega a las tareas
                            #print(t)
                            #print(puntajes[cont].get('usuarioactividad__actividad_id__id_tipo_actividad__tipo'))
                            if puntajes[t]:
                                puntajeList.append(puntajes[t].get('actividades_tipos__usuarioactividad__puntaje_id__puntaje'))
                            else:
                                puntajeList.append('0')
                        finally:
                            cont=cont+1

                else:
                    for t in tipoActividades:
                        puntajeList.append('0')
                alumno.append(puntajeList)
                alumnosList.append(alumno)
                    
            
            
        context={
            'columnas': columnas,
            'alumnos': alumnosList,
            'alumnosEv': alumnosListEv,
            'fechas': '',
            'titulo': 'Resumen Clase '+ fecha
        }
        return render(request, 'puntajes/puntajes_details.html', context)
