from asistencia.models import Asistencia
from evaluacion.models import Evaluacion
from django import forms

#Asistencia

class AsistenciaCreateForm(forms.ModelForm):
    class Meta:
        model=Asistencia
        fields=('fecha',)
        widgets = {
            'fecha': forms.TextInput(attrs={'class':'form-control datepicker',
                                    'placeholder':'Selecciona una fecha',
                                    'type':'text',
                                    'readonly': True},)
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        existe = Asistencia.objects.filter(fecha=fecha).exists()
        if existe:
            self.fields['fecha'].widget.attrs['class'] = 'form-control is-invalid datepicker'
            raise forms.ValidationError("Ya existe una evaluación con esta fecha , ingresa otra fecha")
        return fecha

    #def __init__(self, *args, **kwargs):
    #    super(EvaluacionCreateForm, self).__init__(*args, **kwargs)
    #    self.fields['fecha'].required = True
    
    
