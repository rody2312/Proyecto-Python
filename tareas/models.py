from django.db import models

from app.models import Usuario

# Create your models here.

class TipoArchivo(models.Model):
    tipo=models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_archivo'

    def __str__(self):
        return self.tipo



class PuntajeArchivo(models.Model):
    puntaje=models.IntegerField()

    class Meta:
        managed = True
        db_table = 'puntaje_tarea'

    def __str__(self):
        return self.puntaje



class Tarea(models.Model):
    id_usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    titulo=models.CharField(max_length=50)
    fecha=models.DateField()
    descripcion=models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tarea'


class Archivo(models.Model):
    id_puntaje_archivo=models.ForeignKey(PuntajeArchivo, db_column='id_puntaje_archivo', on_delete=models.CASCADE)
    id_tipo_archivo=models.ForeignKey(TipoArchivo, db_column='id_tipo_archivo', on_delete=models.CASCADE)
    id_tarea=models.ForeignKey(Tarea, db_column='id_tarea', blank=True, null=True, on_delete=models.CASCADE)
    id_usuario=models.ForeignKey(Usuario, db_column='id_usuario', on_delete=models.CASCADE)
    nombre=models.CharField(max_length=20)
    directorio=models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'archivo'
