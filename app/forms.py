from django import forms

from .models import Usuario,TipoUsuario


class UsuarioCreateForm(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=('nombre','apellido_paterno','apellido_materno', 'fono', 'email')
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

        
        