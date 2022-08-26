from django.urls import reverse_lazy
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Notificacion, Usuario
from asistencia.models import UsuarioAsistencia

from evaluacion.models import Evaluacion, UsuarioEvaluacion
from foro.models import Foro
from tareas.models import Archivo, TipoActividad
from tareas.views import obtenerFechas



class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        #Obtener la ultima fecha de la lista de fechas
        fecha = obtenerFechas()[0]

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
                if UsuarioAsistencia.objects.filter(usuario_id=a.id,asistencia__fecha=fecha).exists():
                    alumno.append(UsuarioAsistencia.objects.filter(usuario_id=a.id,asistencia__fecha=fecha).values('tipo_asistencia__puntaje')[0]['tipo_asistencia__puntaje'])
                else:
                    alumno.append('0')

                #Crear lista de puntajes de todas las actividades
                puntajeList= []

                for t in tipoActividades:
                    if TipoActividad.objects.filter(pk=t.id, actividades_tipos__usuarioactividad__usuario_id=a.id,actividades_tipos__fecha=fecha).exists():
                        puntajes = TipoActividad.objects.filter(pk=t.id, actividades_tipos__usuarioactividad__usuario_id=a.id,actividades_tipos__fecha=fecha).values(
                            'actividades_tipos__usuarioactividad__puntaje_id__puntaje')[0]['actividades_tipos__usuarioactividad__puntaje_id__puntaje']
                    else:
                        puntajes = '0'
                    puntajeList.append(puntajes)

                alumno.append(puntajeList)
                alumnosList.append(alumno)


        #Obtener el ultimo archivo subido
        archivo = Archivo.objects.order_by('-fecha').first()

        #Obtener el ultimo foro creado
        foro = Foro.objects.order_by('-fecha').first()

        #Obtener la ultima notificación creada
        notificacion = Notificacion.objects.order_by('-fecha').first()

                    
            
            
        context={
            'columnas': columnas,
            'alumnos': alumnosList,
            'alumnosEv': alumnosListEv,
            'fecha': str(fecha),
            'archivo': archivo,
            'foro': foro,
            'notificacion': notificacion,
        }
        return render(request, 'index.html', context)
