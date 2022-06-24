from cmath import log
from fileinput import filename
from re import A
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DeleteView, UpdateView, CreateView
from app import forms
from app.forms import ArchivoCreateForm
from tareas.models import Archivo
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

#LISTAR ARCHIVO

class ArchivoListView(LoginRequiredMixin ,View):
    
    def get(self,request, *args, **kwargs):
        archivos = Archivo.objects.all()
        context={
            'archivos': archivos,
            'titulo': 'Archivos'
        }
        return render(request, 'archivos/archivo_list.html', context)

#CREAR ARCHIVO
def upload_file(request):
    if request.method == 'POST':
        form = ArchivoCreateForm(request.POST, request.FILES)
        nombre = request.POST['nombre']
        file = request.FILES['directorio']
        fs = FileSystemStorage()

        filename = fs.save(file.name, file)
        #uploaded_file_url = fs.url(filename)

        usuarioActual= request.user
        archivo = Archivo.objects.create(nombre = nombre, directorio = file, id_usuario = usuarioActual)
        archivo.save()
        messages.success(request, "Archivo subido correctamente")
        return redirect('app:archivo')
    else:
        form = ArchivoCreateForm()
    return render(request, 'archivos/archivo_create.html', {'form': form})

class ArchivoCreateView2(LoginRequiredMixin ,CreateView):
    model = Archivo
    form_class = ArchivoCreateForm
    template_name = 'archivos/archivo_create.html'
    success_url: reverse_lazy('erp:archivos/archivo_list.html')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#    def post (self, request, *args, **kwargs):
 #       data = {}
  #      try:
   #         action = request.POST['action']
    #        if action == 'add':
     #           form = self.get._form()
      #          data = form.save()
       #     else:
        #        data['error'] = 'No ha ingresado a ninguna opcion'
        #except Exception as e:
         #   data['error'] = str(e)
        #return JsonResponse(data)

#class ArchivoCreateView(LoginRequiredMixin ,View):
#   
#   def get(self,request, *args, **kwargs):
#       form = ArchivoCreateForm()
#       archivo = Archivo.objects.all()
#       context={
#           'form': form,
#           'titulo': 'Crear Archivo'
#       }
#       return render(request, 'archivos/archivo_create.html', context)
#
#   def post(self, request,*args, **kwargs):
#       if request.method=="POST":
#
#           form = ArchivoCreateForm(request.POST)
#           if form.is_valid():
#               print('Archivo')
#               nombre = form.cleaned_data.get('nombre')
#               archivo = form.cleaned_data.get('directorio')
#               usuarioActual= request.user
#               directorio= 'rafa'
#
#               u, created = Archivo.objects.get_or_create(nombre=nombre, id_usuario=usuarioActual, directorio=archivo)
#               u.save()
#
#               messages.success(request, "Archivo agregado correctamente")
#               return redirect('app:archivo')
#       context={
#           'titulo': 'Crear Archivo',
#           'form': form
#       }
#       return render(request, 'archivos/archivo_create.html', context)

#ELIMINAR ARCHIVO

class ArchivoDeleteView(LoginRequiredMixin, DeleteView):
    model = Archivo
    success_url = reverse_lazy('app:archivo')

    def get_success_url(self):
        messages.success(self.request, "El archivo ha sido eliminado correctamente")
        return reverse('app:archivo')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


