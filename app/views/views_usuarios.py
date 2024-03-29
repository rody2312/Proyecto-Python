from multiprocessing import context
from re import template
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, UpdateView, DeleteView, FormView

from asistencia.models import UsuarioAsistencia
from evaluacion.models import UsuarioEvaluacion
from tareas.models import Actividad, UsuarioActividad
from ..forms import CustomUserCreationForm, UsuarioCreateForm, UsuarioEditForm 
from ..models import Notificacion, TipoUsuario, Usuario
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
import random
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string

from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash

from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from ..utils import token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins import AdminUserMixin, ProfesorUserMixin
import logging

class UsuariosListView(LoginRequiredMixin, AdminUserMixin ,View):
    
    def get(self,request, *args, **kwargs):
        usuarios = Usuario.objects.all()
        context={
            'usuarios': usuarios,
            'titulo': 'Usuarios'
        }
        return render(request, 'usuario/usuarios_list.html', context)


class UsuarioCreateView(LoginRequiredMixin, AdminUserMixin, View):
    def get(self, request,*args, **kwargs):
        form=UsuarioCreateForm()
        context={
            'form':form,
            'titulo': 'Crear Usuario'
        }
        return render(request, 'usuario/usuario_create.html', context)


    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = UsuarioCreateForm(request.POST)
            if form.is_valid():
                logging.warning('Watch out!')
                nombre = form.cleaned_data.get('nombre')
                apellidoPaterno = form.cleaned_data.get('apellido_paterno')
                apellidoMaterno = form.cleaned_data.get('apellido_materno')
                fono = form.cleaned_data.get('fono')
                email = form.cleaned_data.get('email')
                tipo_usuario= form.cleaned_data.get('id_tipo_usuario')
                
                #password = self.randomPassword()
                password = 'admin'
                hashPass = make_password(password)

                u, created = Usuario.objects.get_or_create(nombre=nombre, apellido_paterno=apellidoPaterno, apellido_materno=apellidoMaterno, fono=fono, email=email, id_tipo_usuario=tipo_usuario, password=hashPass)
                u.save()

                domain = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(u.pk))

                link = reverse('app:custom_password_create_confirm', kwargs={'uidb64':uidb64, 'token': token_generator.make_token(u)})
                activate_url = 'http://'+domain+link
                email_body = 'Hola ' + u.nombre + \
                    ' Por favor entra al siguiente link para verificar y crear tu contraseña\n' + activate_url
                # Envio de correo de creación de contraseña
                #template = render_to_string('registration/password_reset_email.html', {
                #    'uid': uidb64,
                #    'token': token_generator.make_token(u),
                #    'domain': domain,
                #    'procotol': 'https'
                #})

                mail = EmailMessage('Crear contraseña', email_body , to=[email])
                mail.send(fail_silently=False)
                messages.success(request, "Usuario agregado correctamente")
                return redirect('app:usuarios')

        
        context={
            'titulo': 'Crear Usuario',
            'form': form
        }
        return render(request, 'usuario/usuario_create.html', context)

    #Funcion para crear una "contraseña" temporal para que se guarde en la bd
    def randomPassword(self):
        characters = list("abcdefghijklmnopqrstuxyz")
        length = 10
        password = ''

        for x in range(length):
            password += random.choice(characters)
        return password


class VerificationView(View):
    def get(self,request,uidb64,token):
        return redirect('app:usuarios')


class UsuarioDetailsView(LoginRequiredMixin, AdminUserMixin, View):
    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Usuario, pk=pk)
        context={
            'usuario':usuario
        }
        return render(request, 'usuario/usuario_details.html', context)

#Clase no usada
class UsuarioUpdateView(LoginRequiredMixin, AdminUserMixin, UpdateView):
    model= Usuario
    fields= ['nombre', 'apellido_paterno', 'apellido_materno']
    template_name= 'usuario/usuario_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('app:details', kwargs={'pk':pk})


class UsuarioDeleteView(LoginRequiredMixin, AdminUserMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('app:usuarios')

    def get_success_url(self):
        messages.success(self.request, "Eliminado correctamente")
        return reverse('app:usuarios')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

#Eliminar usuario##
def deleteUser(request, pk, *args, **kwargs):
    usuario = Usuario.objects.get(id=pk)
    if UsuarioAsistencia.objects.filter(usuario_id=pk).exists() or UsuarioActividad.objects.filter(usuario_id=pk).exists() or UsuarioEvaluacion.objects.filter(usuario_id=pk).exists() or Actividad.objects.filter(pk=pk).exists() or Notificacion.objects.filter(pk=pk).exists():
        messages.error(request, "No se puede eliminar, debido a que existen registros relacionados a '" + str(usuario) + "'")
        return HttpResponseRedirect(reverse_lazy('app:usuarios'))
    else:
        if usuario.delete():
            messages.success(request, "Se elimino correctamente")
        return HttpResponseRedirect(reverse_lazy('app:usuarios'))

class UsuarioEditView(LoginRequiredMixin, AdminUserMixin, UpdateView):
    model = Usuario
    form_class = UsuarioEditForm
    template_name = "usuario/usuario_edit.html"


    def get_success_url(self):
        messages.success(self.request, "El usuario ha sido actualizado correctamente")
        return reverse_lazy('app:usuarios')
        #def get(self, request, pk, *args, **kwargs):
        #    usuario = get_object_or_404(Usuario, pk=pk)
        #    form=UsuarioEditForm(request.POST or None, instance = usuario)
        #    tipos = TipoUsuario.objects.all()
        #    context={
        #        'tipos':tipos,
        #        'usuario':usuario,
        #        'form':form
        #    }
        #    return render(request, 'usuario/usuario_edit.html', context)
        #
        #def post(self, request,*args, **kwargs):
        #    if request.method=="POST":
        #        form = UsuarioEditForm(request.POST)
        #        if form.is_valid():
        #            nombre = form.cleaned_data.get('nombre')
        #            apellidoPaterno = form.cleaned_data.get('apellido_paterno')
        #            apellidoMaterno = form.cleaned_data.get('apellido_materno')
        #            fono = form.cleaned_data.get('fono')
        #            email = form.cleaned_data.get('email')
        #            tipo_usuario= TipoUsuario.objects.get(id=form.cleaned_data['tipo'])
#
        #            u, created = Usuario.objects.update(nombre=nombre, apellido_paterno=apellidoPaterno, apellido_materno=apellidoMaterno, fono=fono, email=email, id_tipo_usuario=tipo_usuario)
        #            u.save()
        #            return redirect('app:usuarios')


class UserChangePasswordView(LoginRequiredMixin, FormView):
    model = Usuario
    form_class = PasswordChangeForm
    template_name = 'usuario/change_password.html'
    success_url = reverse_lazy('app:login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, forma_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'
        return form
  
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de password'
        context['entity'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

#{"error": "'action'"}