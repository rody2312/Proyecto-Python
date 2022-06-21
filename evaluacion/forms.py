from evaluacion.models import Evaluacion
from django import forms

#Evaluacion

class EvaluacionCreateForm(forms.ModelForm):
    class Meta:
        model=Evaluacion
        fields=('titulo','fecha')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.TextInput(attrs={'class':'form-control datepicker',
                                    'placeholder':'Selecciona una fecha',
                                    'type':'text',
                                    'readonly': True},)
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        existe = Evaluacion.objects.filter(fecha=fecha).exists()
        if existe:
            self.fields['fecha'].widget.attrs['class'] = 'form-control is-invalid datepicker'
            raise forms.ValidationError("Ya existe una evaluación con esta fecha , ingresa otra fecha")
        return fecha

    #def __init__(self, *args, **kwargs):
    #    super(EvaluacionCreateForm, self).__init__(*args, **kwargs)
    #    self.fields['fecha'].required = True
    
    
