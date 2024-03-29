from django.core.mail import EmailMessage
from django.core import mail

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView, UpdateView

from core import settings
from ..forms import NotificacionCreateForm
from app import forms
from django.contrib import messages
from app.mixins import AdminProfesorUserMixin, AdminUserMixin, ProfesorUserMixin

from app.models import Notificacion, NotificacionEnviada, Usuario

#LISTAR NOTIFICACION

class NotificacionListView(LoginRequiredMixin ,View):
     
    def get(self,request, *args, **kwargs):

        notificaciones = Notificacion.objects.all().order_by('-fecha')
        context={
            'notificaciones': notificaciones,
            'titulo': 'Notificaciones'
        }
        return render(request, 'notificacion/notificacion_list.html', context)

#CREAR NOTIFICACION

class NotificacionCreateView(LoginRequiredMixin, AdminProfesorUserMixin,View):
    
    def get(self,request, *args, **kwargs):
        form=NotificacionCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Notificacion'
        }
        return render(request, 'notificacion/notificacion_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = NotificacionCreateForm(request.POST)
            if form.is_valid():
                asunto = form.cleaned_data.get('asunto')
                descripcion = form.cleaned_data.get('texto')
                usuarioActual= request.user

                email_body = descripcion

                usuarios = Usuario.objects.all()

                u, created = Notificacion.objects.get_or_create(asunto=asunto, texto=descripcion, enviado_por=usuarioActual)
                u.save()

                #Si la notificación fue creada, enviar notificación a todos los correos de la plataforma
                if created:
                    emails = []
                    connection = mail.get_connection()
                    connection.open()

                    #Se listan todos los usuarios registrados
                    for usuario in usuarios:
                        #Crear mensajes para cada usuario
                        email = EmailMessage('Notificación - Plataforma SCC', email_body , settings.EMAIL_HOST_USER, to=[usuario.email])

                        #Guardar cada notificacion a la bd por cada usuario, individualmente
                        n, n_created = NotificacionEnviada.objects.get_or_create(notificacion=u, enviado_a=usuario)
                        n.save()
                        emails.append(email)

                    connection.send_messages(emails)
                    connection.close()
                    #mail.send(fail_silently=False)
                    messages.success(request, "Notificación agregada correctamente")
                else:
                    messages.error(request, "Hubo un error al intentar agregar la notificación")
                
                return redirect('app:notificacion')
        context={
            'titulo': 'Crear Notificacion',
            'form': form
        }
        return render(request, 'notificacion/notificacion_create.html', context)

#ELIMINAR NOTIFICACION

class NotificacionDeleteView(LoginRequiredMixin,AdminProfesorUserMixin, DeleteView):
    model = Notificacion
    success_url = reverse_lazy('app:notificacion')

    def get_success_url(self):
        messages.success(self.request, "Eliminado correctamente")
        return reverse('app:notificacion')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

#EDITAR NOTIFICACION

class NotificacionEditView(LoginRequiredMixin, AdminProfesorUserMixin, UpdateView):
    model = Notificacion
    form_class = forms.NotificacionCreateForm
    template_name = "notificacion/notificacion_edit.html"

    def get_success_url(self):
        messages.success(self.request, "La notificacion ha sido actualizado correctamente")
        return reverse_lazy('app:notificacion')


#Detalles de la notificación
class NotificacionDetails(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        notificacion = get_object_or_404(Notificacion, pk=pk)

        #Se actualiza la notificacion del usuario de Pendiente a Visto
        NotificacionEnviada.objects.filter(enviado_a=request.user, notificacion=pk).update(estado=2)

        context={
            'notificacion':notificacion
        }
        return render(request, 'notificacion/notificacion_details.html', context)
