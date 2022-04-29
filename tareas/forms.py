
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
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(format=('%d-%m-%Y'), 
                                             attrs={'class':'form-control', 
                                            'placeholder':'Selecciona una fecha',
                                            'type':'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),

        }