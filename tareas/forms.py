
from datetime import date, datetime
from django import forms
from tareas.models import Archivo, Foro, Actividad


class ArchivoCreateForm(forms.ModelForm):

    class Meta:
        model=Archivo
        fields=('nombre', 'directorio')
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'directorio': forms.FileInput(attrs={'class': 'form-control'})

        }



class TareaCreateForm(forms.ModelForm):

    class Meta:
        model=Actividad
        fields=('titulo','fecha',)
        labels={
            'fecha': 'Fecha de la tarea'
        }
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.TextInput(attrs={'class':'form-control datepicker',
                                    'placeholder':'Selecciona una fecha',
                                    'type':'text',
                                    'readonly': True},)
        }

    #def __init__(self, *args, **kwargs):
    #    super(Actividad, self).__init__(*args, **kwargs)
    #    self.fields['fecha2'] = forms.DateField

    def clean_fecha2(self):
        fecha2 = self.cleaned_data.get("fecha2")
        print(fecha2)
        return fecha2
    
    #Falta comparar la fecha anterior con la nueva
    def clean_fecha(self):
        #fecha2 = self.cleaned_data.get("fecha2")
        fecha = self.cleaned_data.get("fecha")
        
        existe = Actividad.objects.filter(fecha=fecha, id_tipo_actividad=1).exists()
        if existe:
            self.fields['fecha'].widget.attrs['class'] = 'form-control is-invalid datepicker'
            self.add_error(('fecha'),forms.ValidationError("Ya existe una tarea con esta fecha , ingresa otra fecha"))
            
        return fecha




class ForoCreateForm(forms.ModelForm):

    class Meta:
        model=Foro
        fields=('titulo', 'descripcion', 'id_tipo_foro', 'id_actividad')
        labels={
            'id_tipo_foro': 'Tipo de privacidad',
            'id_actividad': 'Tarea'
        }
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'id': 'summernote'}),
            'id_tipo_foro': forms.Select(attrs={'class': 'form-control'}),
            'id_actividad': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super(ForoCreateForm, self).__init__(*args, **kwargs)
        self.fields['id_actividad'].required = False