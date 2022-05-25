# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Clase para definir funciones de crear usuarios en el sistema por comando
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        #if not full_name:
        #    raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        #user.full_name = full_name
        user.set_password(password)  # change password to hash
        #user.profile_picture = profile_picture
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user
        

    # ValueError: Cannot assign "'1'": "Usuario.id_tipo_usuario" must be a "TipoUsuario" instance. (?????)
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        #if not full_name:
        #    raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        #user.full_name = full_name
        user.id_tipo_usuario = 1
        user.set_password(password)
        #user.profile_picture = profile_picture
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user


# Aca se definen los modelos

class TipoUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipo_usuario'

    def __str__(self):
        return self.tipo
    



class Usuario(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    id_tipo_usuario = models.ForeignKey(TipoUsuario, models.DO_NOTHING, db_column='id_tipo_usuario')
    nombre = models.CharField(max_length=20, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=30, blank=True, null=True)
    apellido_materno = models.CharField(max_length=30, blank=True, null=True)
    fono = models.IntegerField(blank=True, null=True)
    ciudad = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True, unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=50,unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        managed = True
        db_table = 'usuarios'

class Notificacion(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    texto = models.TextField(null=False)
    fecha = models.DateField(auto_now=True, null=False)

    class Meta():
        managed = True
        db_table = 'notificacion'

class Evaluacion(models.Model):
    titulo = models.TextField(null=False)
    descripcion = models.TextField(null=False)
    fecha = models.DateField(null=False)

    class Meta():
        managed = True
        db_table = 'evaluacion'



