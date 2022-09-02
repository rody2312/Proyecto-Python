from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView, UpdateView
from app.models import Usuario
from asistencia.forms import AsistenciaCreateForm, TipoAsistenciaCreateForm
from asistencia.models import Asistencia, TipoAsistencia, UsuarioAsistencia
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from app.mixins import AdminProfesorUserMixin, AdminUserMixin, ProfesorUserMixin


#Listar registros de asistencias

class AsistenciaListView(LoginRequiredMixin, AdminProfesorUserMixin ,View):
    
    def get(self,request, *args, **kwargs):
        asistencias = Asistencia.objects.all().order_by('-fecha')
        context={
            'asistencias':asistencias,
            'titulo': 'Asistencia'
        }
        return render(request, 'asistencia/asistencia_list.html', context)

#Crear registro de asistencia

class AsistenciaCreateView(LoginRequiredMixin, AdminProfesorUserMixin ,View):
    def get(self,request, *args, **kwargs):
        form=AsistenciaCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Registro de Asistencia'
        }
        return render(request, 'asistencia/asistencia_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = AsistenciaCreateForm(request.POST)
            if form.is_valid():
                fecha = form.cleaned_data.get('fecha')
                
                u, created = Asistencia.objects.get_or_create(fecha=fecha)
                u.save()

                messages.success(request, "Asistencia agregada correctamente")
                return redirect('asistencia:asistencias')

        context={
            'titulo': 'Crear Registro de Asistencia',
            'form': form
        }
        return render(request, 'asistencia/asistencia_create.html', context)


# Eliminar registro de asistencia  
class AsistenciaDeleteView(LoginRequiredMixin, AdminProfesorUserMixin, DeleteView):
    model = Asistencia
    success_url = reverse_lazy('asistencia:asistencias')

    def get_success_url(self):
        messages.success(self.request, "Eliminada correctamente")
        return reverse('asistencia:asistencias')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

# Detalles del registro de asistencia, para registrar el tipo de asistencia a cada alumno
class AsistenciaDetailsView(LoginRequiredMixin, AdminProfesorUserMixin, View):
    def get(self, request, pk, *args, **kwargs):
        asistencia = get_object_or_404(Asistencia, pk=pk)
        context={
            'asistencia': asistencia,
            'titulo': 'Asistencia / Fecha: '+ str(asistencia.fecha)
        }
        return render(request, 'asistencia/asistencia_details.html', context)

class AsistenciaEditView(LoginRequiredMixin, AdminProfesorUserMixin, UpdateView):
    model = Asistencia
    form_class = AsistenciaCreateForm
    template_name = "asistencia/asistencia_create.html"

    def get_success_url(self):
        messages.success(self.request, "La fecha ha sido actualizada correctamente")
        return reverse_lazy('asistencia:asistencias')


#Obtiene los usuarios tipo alumno
@csrf_exempt
def usuariosAsistenciaAPI(request,pk):
    users = Usuario.objects.filter(id_tipo_usuario=3)

    data = []
    #Se verifica la existencia de cada usuario alumno en la tabla de usuario_asistencia, y si no existe, se crea. Y todos se guardan en una lista
    for i in users:
        if not UsuarioAsistencia.objects.prefetch_related('usuario','asistencia','tipo_asistencia').filter(asistencia_id=pk,usuario_id=i.id).exists():
            UsuarioAsistencia.objects.create(asistencia_id=pk,usuario_id=i.id)

        usuarioAsistencia = UsuarioAsistencia.objects.prefetch_related('usuario','asistencia','tipo_asistencia').filter(asistencia_id=pk,usuario_id=i.id)
        #Al realizar la verificación de los usuarios, se guardan en una lista
        #Lista de los usuarios del registro seleccionado
        data.append(usuarioAsistencia)
    
    dataList = []
    asistencia = get_object_or_404(Asistencia, pk=pk)

    #Se obtiene una lista de todos los tipos de asistencia existentes para listarlo en el template
    tipos_asistencia = list(TipoAsistencia.objects.all().values())


    #De la lista creada anteriormente, se realiza otro filtro para enviar datos especificos a la tabla del registro
    for i in data:
        #Capturar los datos de cada alumno
        idUser = i.values('usuario').get()['usuario']
        idTipoAsistencia = i.values('tipo_asistencia').get()['tipo_asistencia']
        usuario = Usuario.objects.get(pk=idUser)

        #Se verifica si el tipo asistencia existe en el registro de asistencia del alumno, en caso de que no exista, se defino como nulo
        try:
            tipo_asistencia = TipoAsistencia.objects.get(pk=idTipoAsistencia)
            tipo_asistencia_nombre = tipo_asistencia.nombre_tipo + ' (' + str(tipo_asistencia.puntaje) + ')'
        except ObjectDoesNotExist:
            tipo_asistencia_nombre = None
        
        nombre = usuario.nombre
        apellido_paterno = usuario.apellido_paterno
        apellido_materno = usuario.apellido_materno

        dataList.append({'id':idUser,'nombre':nombre, 'apellido_paterno':apellido_paterno, 'apellido_materno':apellido_materno,
                        'puntajeID':idTipoAsistencia, 'puntaje':tipo_asistencia_nombre, 'opcionesPuntaje':tipos_asistencia})
    return JsonResponse(dataList, safe=False)

#Actualiza el registro individual de la asistencia
@csrf_exempt
def updatePuntaje(request):
    userID = request.POST.get('usuario')
    tipoAsistenciaID = request.POST.get('puntaje')
    #puntajeObject = get_object_or_404(Puntaje, pk=puntajeID)
    asistenciaID = request.POST.get('asistencia')

    if tipoAsistenciaID == '0':
        tipoAsistenciaID = None

    if UsuarioAsistencia.objects.filter(usuario=userID, asistencia=asistenciaID).exists():
        UsuarioAsistencia.objects.filter(usuario=userID, asistencia=asistenciaID).update(tipo_asistencia=tipoAsistenciaID)
    else:
        usuarioAsistencia = UsuarioAsistencia.objects.get_or_create(usuario=userID, asistencia=asistenciaID)
        usuarioAsistencia.tipo_asistencia = tipoAsistenciaID
        usuarioAsistencia.save()

    return JsonResponse('Puntaje actualizado', safe=False)


# Listar tipos de asistencia
class TipoAsistenciaListView(LoginRequiredMixin, AdminUserMixin,View):
     
    def get(self,request, *args, **kwargs):

        tipos_asistencia = TipoAsistencia.objects.all()
        context={
            'tipos_asistencia': tipos_asistencia,
            'titulo': 'Tipos de Asistencia'
        }
        return render(request, 'asistencia/tipo_asistencia_list.html', context)

#CREAR TIPO ACTIVIDAD

class TipoAsistenciaCreateView(LoginRequiredMixin, AdminUserMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form=TipoAsistenciaCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Tipo de Actividad'
        }
        return render(request, 'asistencia/tipo_asistencia_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = TipoAsistenciaCreateForm(request.POST)
            if form.is_valid():
                nombre_tipo = form.cleaned_data.get('nombre_tipo')
                puntaje = form.cleaned_data.get('puntaje')

                u, created = TipoAsistencia.objects.get_or_create(nombre_tipo=nombre_tipo, puntaje=puntaje)
                u.save()

                messages.success(request, "Tipo de actividad agregada correctamente")
                return redirect('asistencia:list_tipo_asistencia')
        context={
            'titulo': 'Crear tipo asistencia',
            'form': form
        }
        return render(request, 'asistencia/tipo_asistencia_create.html', context)


#Eliminar tipo de asistencia SI USAR##
def delete(request, pk, *args, **kwargs):
    tipo = TipoAsistencia.objects.get(id=pk)
    if UsuarioAsistencia.objects.filter(tipo_asistencia=pk).exists():
        messages.error(request, "No se puede eliminar, debido a que existen registros de asistencias relacionados a '" + tipo.nombre_tipo + "'")
        return HttpResponseRedirect(reverse_lazy('asistencia:list_tipo_asistencia'))
    else:
        if tipo.delete():
            messages.success(request, "Se elimino correctamente")
        return HttpResponseRedirect(reverse_lazy('asistencia:list_tipo_asistencia'))

#EDITAR TIPO ACTIVIDAD

class TipoAsistenciaEditView(LoginRequiredMixin, AdminUserMixin, UpdateView):
    model = TipoAsistencia
    form_class = TipoAsistenciaCreateForm
    template_name = "asistencia/tipo_asistencia_edit.html"

    def get_success_url(self):
        messages.success(self.request, "El tipo de asistencia ha sido actualizado correctamente")
        return reverse_lazy('asistencia:list_tipo_asistencia')