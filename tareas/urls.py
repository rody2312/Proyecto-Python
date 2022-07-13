from django.urls import path
from .views import *

app_name="tareas"

urlpatterns = [
    #Tareas
    path('tareas/<int:tipo_id>/', TareasListView.as_view(), name='tareas'),
    path('tareas/crear/<int:tipo_id>/', TareasCreateView.as_view(), name='crear_tarea'),
    path('tareas/detalles/<int:pk>/', TareaDetailsView.as_view(), name="details"),
    path('tareas/edit/<int:pk>/', TareaEditView.as_view(), name="edit"),
    path('tareas/delete/<int:pk>/', TareaDeleteView.as_view(), name="delete"),
    path('actividadPuntajesAPI/<int:pk>/', usuariosActividadAPI),
    path('updatePuntaje/', updatePuntaje),

    #Resumen de puntajes
    path('resumen/', ResumenListView.as_view(), name="resumen"),
    path('resumen/<str:fecha>/', ResumenDetailsView.as_view(), name="resumen_detalles"),
]
