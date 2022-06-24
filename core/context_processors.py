from tareas.models import TipoActividad


def load_navbar_tipos(request):
    tiposActividades = TipoActividad.objects.all()
    return {'tipos_actividades_nabvar': tiposActividades}