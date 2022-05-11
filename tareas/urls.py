from django.urls import path
from .views import *

app_name="tareas"

urlpatterns = [
    path('tareas/', TareasListView.as_view(), name='tareas'),
    path('tareas/create', TareasCreateView.as_view(), name='crear_tarea'),
    path('tareas/details/<int:pk>/', TareaDetailsView.as_view(), name="details"),
    path('tareas/edit/<int:pk>/', TareaEditView.as_view(), name="edit"),
    path('tareas/delete/<int:pk>/', TareaDeleteView.as_view(), name="delete"),
]
