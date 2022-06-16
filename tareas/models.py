from django.db import models

from app.models import Usuario

# Create your models here.

class TipoActividad(models.Model):
    tipo=tipo = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'tipo_actividad'

    def __str__(self):
        return self.tipo

class Actividad(models.Model):
    id_tipo_actividad=models.ForeignKey(TipoActividad, on_delete=models.SET_NULL, db_column='id_tipo_actividad', null=True)
    id_usuario=models.ForeignKey(Usuario, on_delete=models.SET_NULL, db_column='id_usuario', null=True)
    titulo = models.CharField(max_length=50)
    fecha=models.DateField()

    class Meta:
        managed = True
        db_table = 'actividad'

    def __str__(self):
        return str(self.fecha)

class TipoForo(models.Model):
    tipo=tipo = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'tipo_foro'

    def __str__(self):
        return self.tipo

class Foro(models.Model):
    id_tipo_foro=models.ForeignKey(TipoForo, db_column='id_tipo_foro', on_delete=models.PROTECT)
    id_actividad=models.ForeignKey(Actividad, db_column='id_actividad', on_delete=models.SET_NULL, null=True)
    titulo=models.CharField(max_length=50)
    descripcion=models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'foro'


class Archivo(models.Model):
    id_usuario=models.ForeignKey(Usuario, db_column='id_usuario', on_delete=models.CASCADE)
    nombre=models.CharField(max_length=20)
    directorio=models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'archivo'
