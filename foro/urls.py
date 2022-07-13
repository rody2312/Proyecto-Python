from django.urls import path
from .views import *

app_name="foro"

urlpatterns = [
    
    #Foro
    path('foro/', ForosListView.as_view(), name="foros"),
    path('foro/borrar/<int:pk>/', ForoDeleteView.as_view(), name="foro_delete"),
    path('foro/crear/', ForoCreateView.as_view(), name="crear_foro"),
    path('foro/edit/<int:pk>/', ForoEditView.as_view(), name="foro_edit"),
    path('foro/<int:pk>/', ForoDetailsView.as_view(), name="foro_details"),

    path('foro/<int:pk>/responder', ForoResponderView.as_view(), name="responder_foro"),

]
