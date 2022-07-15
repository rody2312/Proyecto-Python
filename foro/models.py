from django.db import models
from app.models import Usuario

from tareas.models import Actividad
from django.utils import timezone

# Create your models here.

class TipoForo(models.Model):
    tipo=tipo = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'tipo_foro'

    def __str__(self):
        return self.tipo

class Foro(models.Model):
    id_tipo_foro=models.ForeignKey(TipoForo, db_column='id_tipo_foro', on_delete=models.PROTECT)
    id_actividad=models.ForeignKey(Actividad, db_column='id_actividad', on_delete=models.SET_NULL, null=True, unique=True)
    titulo=models.CharField(max_length=50)
    descripcion=models.TextField(blank=True, null=True)
    fecha=models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'foro'


class RespuestaForo(models.Model):
    id_usuario=models.ForeignKey(Usuario, db_column='id_usuario', on_delete=models.SET_NULL, null=True)
    id_foro=models.ForeignKey(Foro, related_name='comments', db_column='id_foro', on_delete=models.CASCADE, null=True)
    texto=models.TextField(blank=True, null=True)
    fecha=models.DateTimeField(default=timezone.now, editable=False, blank=True)

    class Meta:
        managed = True
        db_table = 'respuesta_foro'