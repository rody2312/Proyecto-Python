from django.urls import path
from .views import *

app_name="tareas"

urlpatterns = [
    #Tareas
    path('tareas/', TareasListView.as_view(), name='tareas'),
    path('tareas/create', TareasCreateView.as_view(), name='crear_tarea'),
    path('tareas/details/<int:pk>/', TareaDetailsView.as_view(), name="details"),
    path('tareas/edit/<int:pk>/', TareaEditView.as_view(), name="edit"),
    path('tareas/delete/<int:pk>/', TareaDeleteView.as_view(), name="delete"),
    
    #Foro
    path('tareas/crear_foro/<int:pk>/', ForoCreateView.as_view(), name="crear_foro"),
    path('tareas/foro/<int:pk>/', ForoDetailsView.as_view(), name="foro_details"),

    #Caja de preguntas
    path('caja-preguntas/', CajaDePreguntasListView.as_view(), name="caja_preguntas_list"),
    path('caja-preguntas/create/', CajaDePreguntasCreateView.as_view(), name="crear_caja_preguntas"),
    path('caja-preguntas/delete/<int:pk>/', CajaDePreguntasDeleteView.as_view(), name="caja_preguntas_delete"),

]
