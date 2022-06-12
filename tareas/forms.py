
from datetime import date, datetime
from django import forms
from tareas.models import Archivo, Foro, Tarea


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
        model=Tarea
        fields=('fecha',)
        labels={
            'fecha': 'Fecha de la tarea'
        }
        
        widgets = {
            'fecha': forms.DateInput(attrs={'class':'form-control', 
                                    'placeholder':'Selecciona una fecha',
                                    'type':'date'},
                                    format = '%d/%m/%Y')
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        existe = Tarea.objects.filter(fecha=fecha, id_tipo_tarea=1).exists()
        if existe:
            self.fields['fecha'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError("Ya existe una tarea con esta fecha , ingresa otra fecha")
        return fecha


class CajaDePreguntasCreateForm(forms.ModelForm):

    class Meta:
        model=Tarea
        fields=('fecha',)
        labels={
            'fecha': 'Fecha de la tarea'
        }
        
        widgets = {
            'fecha': forms.DateInput(attrs={'class':'form-control', 
                                    'placeholder':'Selecciona una fecha',
                                    'type':'date'},
                                    format = '%d/%m/%Y')
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        existe = Tarea.objects.filter(fecha=fecha, id_tipo_tarea=2).exists()
        if existe:
            self.fields['fecha'].widget.attrs['class'] = 'form-control is-invalid'
            raise forms.ValidationError("Ya existe una tarea con esta fecha , ingresa otra fecha")
        return fecha


class ForoCreateForm(forms.ModelForm):

    class Meta:
        model=Foro
        fields=('titulo', 'descripcion', 'id_tipo_foro', 'id_tarea')
        labels={
            'id_tipo_foro': 'Tipo de privacidad',
            'id_tarea': 'Tarea'
        }
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'id': 'summernote'}),
            'id_tipo_foro': forms.Select(attrs={'class': 'form-control'}),
            'id_tarea': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super(ForoCreateForm, self).__init__(*args, **kwargs)
        self.fields['id_tarea'].required = False