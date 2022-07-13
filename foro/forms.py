
from foro.models import Foro, RespuestaForo
from django import forms

class ForoCreateForm(forms.ModelForm):

    class Meta:
        model=Foro
        fields=('titulo', 'descripcion', 'id_tipo_foro',)
        labels={
            'id_tipo_foro': 'Tipo de privacidad',
        }
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'id': 'summernote'}),
            'id_tipo_foro': forms.Select(attrs={'class': 'form-control'}),
        }
    
    #def __init__(self, *args, **kwargs):
    #    super(ForoCreateForm, self).__init__(*args, **kwargs)
    #    self.fields['id_actividad'].required = False


class ForoRespuestaForm(forms.ModelForm):

    class Meta:
        model=RespuestaForo
        fields=('texto',)
        labels={
            'texto': 'Realiza tu respuesta al foro',
        }
        
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'id': 'summernote'}),
        }


    def __init__(self, *args, **kwargs):
        super(ForoRespuestaForm, self).__init__(*args, **kwargs)
        self.fields['texto'].required = True
