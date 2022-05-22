
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


class ForoCreateForm(forms.ModelForm):

    class Meta:
        model=Foro
        fields=('titulo', 'descripcion', 'id_tipo_foro')
        labels={
            'id_tipo_foro': 'Tipo de privacidad',
        }
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'id_tipo_foro': forms.Select(attrs={'class': 'form-control'})
        }