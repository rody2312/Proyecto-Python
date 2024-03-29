
from cProfile import label
from django import forms

from tareas.models import Archivo, Puntaje, TipoActividad
from .models import Notificacion, Usuario,TipoUsuario


from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ValidationError
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class UsuarioCreateForm(forms.ModelForm):

    class Meta:
        model=Usuario
        fields=('nombre','apellido_paterno','apellido_materno', 'fono', 'email', 'id_tipo_usuario')
        labels = {
            'id_tipo_usuario':'Tipo de usuario'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'fono': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'id_tipo_usuario': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        existe = Usuario.objects.filter(email=email).exists()
        if existe:
            self.fields['email'].widget.attrs['class'] = 'form-control is-invalid'
            raise ValidationError("Este correo ya esta existe, ingresa otro correo")
        return email

    def __init__(self, *args, **kwargs):
        super(UsuarioCreateForm, self).__init__(*args, **kwargs)
        #tipos = TipoUsuario.objects.all()
        #tiposUsuario = [(t.id, t.tipo) for t in tipos]
        #self.fields['tipo'] = forms.ChoiceField(choices=tiposUsuario)
        #self.fields['tipo'].widget.attrs['class'] = 'form-control'
        self.fields['nombre'].required = True
        self.fields['apellido_paterno'].required = True
        self.fields['apellido_materno'].required = True
        self.fields['fono'].required = True
        self.fields['email'].required = True
        self.fields['id_tipo_usuario'].required = True


#class UserProfileForm(ModelForm)
#c   def __init__(self, *args, **kwargs):
#c
#c   class Meta:
#c       model = Usuario
#c       fields = 'nombre', 'apellido_paterno', 'apellido_materno', 'fono', 'email', 'id_tipo_usuario'
#c       widgets = {}
#c           'nombre': forms.TextInput(attrs='class': 'form-control'),
#
#
#
#   def save(self, commit = True):
#       data = {}
#       form = super()
#       try:
#           if form.is_valid():
#               pwd = self.cleaned_data['password']
#               u = form.save(commit=False)
#               if u.pk is None:
#                   u.set_password(pwd)
#               else:
#                   user = Usuario.objects.get(pk=u.pk)
#                   if user.password != pwd:
#                       u.set_password(pwd)
#               u.save()
#           else:
#               data['error'] = form.errors
#       except Exception as e:
#           data['error'] = str(e)
#       return data














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
        fields=('asunto','texto',)

        widgets = {
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(NotificacionCreateForm, self).__init__(*args, **kwargs)
        self.fields['asunto'].required = True
        self.fields['texto'].required = True


#Forms para sección de configuraciones (Cambiar a app de tareas)

class TipoActividadCreateForm(forms.ModelForm):
    class Meta:
        model=TipoActividad
        fields=('tipo',)

        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TipoActividadCreateForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].required = True


class PuntajeCreateForm(forms.ModelForm):
    class Meta:
        model=Puntaje
        fields=('puntaje',)

        widgets = {
            'puntaje': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    #def __init__(self, *args, **kwargs):
    #    super(TipoActividadCreateForm, self).__init__(*args, **kwargs)
    #    self.fields['tipo'].required = True


        

#Subir archivo
class ArchivoCreateForm(forms.ModelForm):
   class Meta:
       model=Archivo
       fields=('nombre','directorio',)
       labels = {
            'directorio':'Subir archivo'
        }
       widgets = {
           'nombre': forms.TextInput(attrs={'class': 'form-control'}),
           'directorio': forms.ClearableFileInput(attrs={'class': 'form-control', 'id':'directorio'}),
        }

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


class CambiarPassForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("Las dos contraseñas ingresadas no coinciden."),
    }
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":"form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":"form-control"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ResetPassForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control"}),
    )

