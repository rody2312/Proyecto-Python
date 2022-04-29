from django import forms
from .models import Notificacion, Usuario,TipoUsuario


from django.contrib.auth.forms import UserCreationForm


class UsuarioCreateForm(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=('nombre','apellido_paterno','apellido_materno', 'fono', 'email','password')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'fono': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioCreateForm, self).__init__(*args, **kwargs)
        tipos = TipoUsuario.objects.all()
        tiposUsuario = [(t.id, t.tipo) for t in tipos]
        self.fields['tipo'] = forms.ChoiceField(choices=tiposUsuario)
        self.fields['tipo'].widget.attrs['class'] = 'form-control'
        self.fields['nombre'].required = True
        self.fields['apellido_paterno'].required = True
        self.fields['apellido_materno'].required = True
        self.fields['fono'].required = True
        self.fields['email'].required = True
        self.fields['tipo'].required = True


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=Usuario
        fields=('nombre','apellido_paterno','apellido_materno', 'fono', 'email','password')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'fono': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        } 

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        tipos = TipoUsuario.objects.all()
        tiposUsuario = [(t.id, t.tipo) for t in tipos]
        self.fields['tipo'] = forms.ChoiceField(choices=tiposUsuario)
        self.fields['tipo'].widget.attrs['class'] = 'form-control'
        self.fields['nombre'].required = True
        self.fields['apellido_paterno'].required = True
        self.fields['apellido_materno'].required = True
        self.fields['fono'].required = True
        self.fields['email'].required = True
        self.fields['tipo'].required = True  
        

class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=('nombre','apellido_paterno','apellido_materno', 'fono', 'email','id_tipo_usuario')
        labels = {
            'id_tipo_usuario':'Tipo de usuario'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'fono': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'id_tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioEditForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['apellido_paterno'].required = True
        self.fields['apellido_materno'].required = True
        self.fields['fono'].required = True
        self.fields['email'].required = True
        self.fields['id_tipo_usuario'].required = True


class NotificacionCreateForm(forms.ModelForm):
    class Meta:
        model=Notificacion
        fields=('texto','id_usuario')
        labels = {
            'id_usuario':'Usuario'
        }
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'form-control'}),
            'id_usuario': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(NotificacionCreateForm, self).__init__(*args, **kwargs)
        self.fields['texto'].required = True
        self.fields['id_usuario'].required = True



#class ArchivoCreateForm(forms.ModelForm):
 #   class Meta:
  #      model=Archivo
   #     fields=('n de archivo','nombre de archivo','fecha de subida', 'descargar')
    #    widgets = {
     #       'n de archivo': forms.TextInput(),
      #      'nombre de archivo': forms.TextInput(),
       #     'fecha de subida': forms.TextInput(),
        #    'descargar': forms.DateInput(),
#        }

 #   def __init__(self, *args, **kwargs):
  #      super(ArchivoCreateForm, self).__init__(*args, **kwargs)
   #     tipos = TipoUsuario.objects.all()
    #    tiposUsuario = [(t.id, t.tipo) for t in tipos]
     #   self.fields['tipo'] = forms.ChoiceField(choices=tiposUsuario)
      #  self.fields['tipo'].widget.attrs['class'] = 'form-control'
       # self.fields['n de archivo'].required = True
        #self.fields['nombre de archivo'].required = True
        #self.fields['fecha de subida'].required = True
     #   self.fields['descargar'].required = True