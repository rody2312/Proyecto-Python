from django.db import models

from app.models import Usuario

# Create your models here.

class Evaluacion(models.Model):
    id_usuario=models.ForeignKey(Usuario, on_delete=models.SET_NULL, db_column='id_usuario', null=True, related_name='usuario_crea_ev')
    titulo = models.CharField(max_length=50)
    fecha=models.DateField(unique=True)
    usuarios=models.ManyToManyField(Usuario, through='UsuarioEvaluacion', related_name='usuario_evaluaciones')

    class Meta:
        managed = True
        db_table = 'evaluacion'

class PuntajeEvaluacion(models.Model):
    puntaje = models.SmallIntegerField()
    
    class Meta:
        managed = True
        db_table = 'puntaje_evaluacion'


class UsuarioEvaluacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    puntaje = models.ForeignKey(PuntajeEvaluacion, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = 'usuario_evaluacion'
    
    def __str__(self):
        return str(str(self.usuario) + ' ' + str(self.actividad) + ' ' + str(self.puntaje))