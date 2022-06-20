from evaluacion.models import Evaluacion
from django import forms

#Evaluacion

class EvaluacionCreateForm(forms.ModelForm):
    class Meta:
        model=Evaluacion
        fields=('titulo','fecha')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class':'form-control', 
                                            'placeholder':'Selecciona una fecha',
                                            'type':'date'},
                                                format = '%d/%m/%Y')
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        existe = Evaluacion.objects.filter(fecha=fecha).exists()
        if existe:
            self.fields['fecha'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError("Ya existe una evaluación con esta fecha , ingresa otra fecha")
        return fecha

    def __init__(self, *args, **kwargs):
        super(EvaluacionCreateForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].required = True
        self.fields['fecha'].required = True
    
    
