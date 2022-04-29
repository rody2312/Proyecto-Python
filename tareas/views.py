from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from tareas.forms import ArchivoCreateForm, TareaCreateForm

from tareas.models import Tarea

# Create your views here.

class TareasListView(LoginRequiredMixin, View):

    def get(self,request, *args, **kwargs):
        tareas = Tarea.objects.all()
        context={
            'tareas': tareas,
            'titulo': 'Tareas'
        }
        return render(request, 'tareas/tareas_list.html', context)



class TareasCreateView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        form = TareaCreateForm()
        context={
            'form': form,
            'titulo': 'Crear Tarea'
        }
        return render(request, 'tareas/tarea_create.html', context)

    def post(self, request,*args, **kwargs):
        if request.method=="POST":
            form = TareaCreateForm(request.POST)
            if form.is_valid():
                titulo = form.cleaned_data.get('titulo')
                fecha = form.cleaned_data.get('fecha')
                descripcion = form.cleaned_data.get('descripcion')
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