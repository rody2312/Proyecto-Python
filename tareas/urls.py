from django.urls import path
from .views import *

app_name="tareas"

urlpatterns = [
    path('tareas/', TareasListView.as_view(), name='tareas'),
]
