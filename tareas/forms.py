
from datetime import date, datetime
from django import forms
from tareas.models import Archivo, Tarea


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
        fields=('titulo', 'fecha', 'descripcion')
        labels={
            'fecha': 'Fecha de la tarea'
        }
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class':'form-control', 
                                    'placeholder':'Selecciona una fecha',
                                    'type':'date'},
                                    format = '%d/%m/%Y'),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),

        }