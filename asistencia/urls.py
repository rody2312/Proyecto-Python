from django.urls import path
from .views import *

app_name="asistencia"

urlpatterns = [
    #Asistencia
    path('asistencia/', AsistenciaListView.as_view(), name="asistencias"),
    path('asistencia/crear/', AsistenciaCreateView.as_view(), name="crear_asistencia"),
    path('asistencia/details/<int:pk>/', AsistenciaDetailsView.as_view(), name="asistencia_details"),
    path('asistencia/eliminar/<int:pk>/', AsistenciaDeleteView.as_view(), name="asistencia_delete"),
    path('asistencia/editar/<int:pk>/', AsistenciaEditView.as_view(), name="asistencia_edit"),
    path('asistenciaPuntajesAPI/<int:pk>/', usuariosAsistenciaAPI),
    path('updatePuntajeAsis/', updatePuntaje),

    #Tipos de Asistencia
    path('tipo_asistencia/', TipoAsistenciaListView.as_view(), name="list_tipo_asistencia"),
    path('tipo_asistencia/create/', TipoAsistenciaCreateView.as_view(), name="crear_tipo_asistencia"),
    path('tipo_asistencia/delete/<int:pk>/', delete, name="delete_tipo_asistencia"),
    path('tipo_asistencia/edit/<int:pk>/', TipoAsistenciaEditView.as_view(), name="edit_tipo_asistencia"),
]