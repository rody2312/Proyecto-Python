from django.contrib import admin

# Register your models here.

from .models import TipoUsuario, Usuario

admin.site.register(Usuario)
admin.site.register(TipoUsuario)