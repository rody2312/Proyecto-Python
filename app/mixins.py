from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse


class AdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id_tipo_usuario.id == 1
        
    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Solo los administradores pueden acceder a este interfaz',
            'tipo': str(self.request.user.id_tipo_usuario)}
        )

class ProfesorUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id_tipo_usuario.id == 2
        
    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Solo los profesores pueden acceder a este interfaz',
            'tipo': str(self.request.user.id_tipo_usuario)}
        )

class AdminProfesorUserMixin(UserPassesTestMixin):
    def test_func(self):
        return AdminUserMixin.test_func(self) or ProfesorUserMixin.test_func(self)
        
    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Solo los usuarios con permisos pueden acceder a este interfaz',
            'tipo': str(self.request.user.id_tipo_usuario)}
        )

class AlumnoUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id_tipo_usuario.id == 3
        
    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Solo los alumnos pueden acceder a este interfaz',
            'tipo': str(self.request.user.id_tipo_usuario)}
        )