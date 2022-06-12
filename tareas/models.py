from django.db import models

from app.models import Usuario

# Create your models here.

class TipoTarea(models.Model):
    tipo=tipo = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'tipo_tarea'

    def __str__(self):
        return self.tipo

class Tarea(models.Model):
    id_tipo_tarea=models.ForeignKey(TipoTarea, on_delete=models.CASCADE, db_column='id_tipo_tarea')
    id_usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    fecha=models.DateField()

    class Meta:
        managed = True
        db_table = 'tarea'

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
    id_tarea=models.ForeignKey(Tarea, db_column='id_tarea', on_delete=models.SET_NULL, null=True)
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
