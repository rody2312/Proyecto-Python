from django.db import models

from app.models import Usuario

# Create your models here.

class Asistencia(models.Model):
    fecha=models.DateField(unique=True)
    usuarios=models.ManyToManyField(Usuario, through='UsuarioAsistencia', related_name='usuario_asistencias')
    
    class Meta:
        managed = True
        db_table = 'asistencia'

class TipoAsistencia(models.Model):
    nombre_tipo = models.CharField(max_length=30)
    puntaje = models.SmallIntegerField()

    class Meta:
        managed = True
        db_table = 'tipo_asistencia'

class UsuarioAsistencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    asistencia = models.ForeignKey(Asistencia, on_delete=models.CASCADE)
    tipo_asistencia = models.ForeignKey(TipoAsistencia, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = 'usuario_asistencia'
