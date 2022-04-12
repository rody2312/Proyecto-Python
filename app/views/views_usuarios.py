from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, UpdateView, DeleteView
from ..forms import UsuarioCreateForm
from ..models import TipoUsuario, Usuario
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.
class UsuariosListView(View):
    def get(self,request, *args, **kwargs):
        usuarios = Usuario.objects.all()
        context={
            'usuarios': usuarios,
            'titulo': 'Usuarios'
        }
        return render(request, 'usuario/usuarios_list.html', context)


class UsuarioCreateView(View):
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
                nombre = form.cleaned_data.get('nombre')
                apellidoPaterno = form.cleaned_data.get('apellido_paterno')
                apellidoMaterno = form.cleaned_data.get('apellido_materno')
                fono = form.cleaned_data.get('fono')
                email = form.cleaned_data.get('email')
                tipo_usuario= TipoUsuario.objects.get(id=form.cleaned_data['tipo'])

                u, created = Usuario.objects.get_or_create(nombre=nombre, apellido_paterno=apellidoPaterno, apellido_materno=apellidoMaterno, fono=fono, email=email, id_tipo_usuario=tipo_usuario)
                u.save()
                return redirect('app:usuarios')


        context={

        }
        return render(request, 'usuario/usuario_create.html', context)


class UsuarioDetailsView(View):
    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Usuario, pk=pk)
        context={
            'usuario':usuario
        }
        return render(request, 'usuario/usuario_details.html', context)

class UsuarioUpdateView(UpdateView):
    model= Usuario
    fields= ['nombre', 'apellido_paterno', 'apellido_materno']
    template_name= 'usuario/usuario_update.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('app:details', kwargs={'pk':pk})


class UsuarioDeleteView(DeleteView):
    model = Usuario
    success_url = reverse_lazy('app:usuarios')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Eliminado correctamente")
        return HttpResponseRedirect(success_url) 

class UsuarioEditView(View):
        def get(self, request, pk, *args, **kwargs):
            usuario = get_object_or_404(Usuario, pk=pk)
            context={
                'usuario':usuario
            }
            return render(request, 'usuario/usuario_edit.html', context)