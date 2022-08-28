from app.models import NotificacionEnviada
from tareas.models import TipoActividad


def load_navbar_tipos(request):
    tiposActividades = TipoActividad.objects.all()
    return {'tipos_actividades_nabvar': tiposActividades}


def load_notifications(request):

    #Obtener las ultimas 5 notificaciones enviadas
    if request.user.is_authenticated:
        notificaciones = NotificacionEnviada.objects.filter(enviado_a=request.user).order_by('-notificacion__fecha')[:5]
        cant_pendientes = NotificacionEnviada.objects.filter(enviado_a=request.user, estado=1).count()
    else:
        notificaciones = None
        cant_pendientes = None

    return {'notificaciones_nav': notificaciones, 'cant_pendientes': cant_pendientes}