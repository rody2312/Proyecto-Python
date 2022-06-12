from django.urls import path
from .views import *

app_name="tareas"

urlpatterns = [
    #Tareas
    path('tareas/', TareasListView.as_view(), name='tareas'),
    path('tareas/create/', TareasCreateView.as_view(), name='crear_tarea'),
    path('tareas/details/<int:pk>/', TareaDetailsView.as_view(), name="details"),
    path('tareas/edit/<int:pk>/', TareaEditView.as_view(), name="edit"),
    path('tareas/delete/<int:pk>/', TareaDeleteView.as_view(), name="delete"),
    
    #Foro
    path('foro/', ForosListView.as_view(), name="foros"),
    path('foro/borrar/<int:pk>/', ForoDeleteView.as_view(), name="foro_delete"),
    path('foro/crear/', ForoCreateView.as_view(), name="crear_foro"),
    path('foro/edit/<int:pk>/', ForoEditView.as_view(), name="foro_edit"),
    path('foro/<int:pk>/', ForoDetailsView.as_view(), name="foro_details"),

    #Caja de preguntas
    path('caja-preguntas/', CajaDePreguntasListView.as_view(), name="caja_preguntas_list"),
    path('caja-preguntas/create/', CajaDePreguntasCreateView.as_view(), name="crear_caja_preguntas"),
    path('caja-preguntas/delete/<int:pk>/', CajaDePreguntasDeleteView.as_view(), name="caja_preguntas_delete"),

]
