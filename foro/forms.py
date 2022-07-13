
from foro.models import Foro
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