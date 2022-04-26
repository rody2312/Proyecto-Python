from re import template
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, UpdateView, DeleteView
from ..forms import CustomUserCreationForm, UsuarioCreateForm, UsuarioEditForm 
from ..models import TipoUsuario, Usuario
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
import random
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string

from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from ..utils import token_generator
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class UsuariosListView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        usuarios = Usuario.objects.all()
        context={
            'usuarios': usuarios,
            'titulo': 'Usuarios'
        }
        return render(request, 'usuario/usuarios_list.html', context)


class UsuarioCreateView(LoginRequiredMixin, View):
    def get(self, request,*args, **kwargs):
        form=CustomUserCreationForm()
        context={
            'form':form,
            'titulo': 'Crear Usuario'
        }
        return render(request, 'usuario/usuario_create.html', context)


    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = UsuarioCreateForm(request.POST)
            if form.is_valid():
                nombre = form.cleaned_data.get('nombre')
                apellidoPaterno = form.cleaned_data.get('apellido_paterno')
                apellidoMaterno = form.cleaned_data.get('apellido_materno')
                fono = form.cleaned_data.get('fono')
                email = form.cleaned_data.get('email')
                tipo_usuario= TipoUsuario.objects.get(id=form.cleaned_data['tipo'])
                
                #password = self.randomPassword()
                password = 'admin'
                hashPass = make_password(password)

                u, created = Usuario.objects.get_or_create(nombre=nombre, apellido_paterno=apellidoPaterno, apellido_materno=apellidoMaterno, fono=fono, email=email, id_tipo_usuario=tipo_usuario, password=hashPass)
                u.save()

                domain = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(u.pk))

                link = reverse('app:password_reset_confirm', kwargs={'uidb64':uidb64, 'token': token_generator.make_token(u)})
                activate_url = 'http://'+domain+link
                email_body = 'Hola' + u.nombre + \
                    'Por favor entra al siguiente link para verificar y crear tu contraseña\n' + activate_url
                # Envio de correo de creación de contraseña
                #template = render_to_string('registration/password_reset_email.html', {
                #    'uid': uidb64,
                #    'token': token_generator.make_token(u),
                #    'domain': domain,
                #    'procotol': 'https'
                #})

                mail = EmailMessage('Crear contraseña', email_body , to=[email])
                mail.send(fail_silently=False)
                return redirect('app:usuarios')


        context={

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


class UsuarioDetailsView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Usuario, pk=pk)
        context={
            'usuario':usuario
        }
        return render(request, 'usuario/usuario_details.html', context)

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model= Usuario
    fields= ['nombre', 'apellido_paterno', 'apellido_materno']
    template_name= 'usuario/usuario_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('app:details', kwargs={'pk':pk})


class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('app:usuarios')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Eliminado correctamente")
        return HttpResponseRedirect(success_url)

#def eliminar_usuario(request,id):
#    usuario = get_object_or_404(Usuario, id=id)
#    usuario.delete()
#    return redirect(to="app:usuarios")

class UsuarioEditView(LoginRequiredMixin, UpdateView):
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