from evaluacion.views import EvaluacionDeleteView, EvaluacionDetailsView, EvaluacionListView, EvaluacionCreateView
from django.urls import path

app_name="evaluacion"

urlpatterns= [

    #EVALUACION
    path('evaluacion/', EvaluacionListView.as_view(), name="evaluaciones"),
    path('evaluacion_create/', EvaluacionCreateView.as_view(), name="crear_evaluacion"),
    path('evaluacion/details/<int:pk>/', EvaluacionDetailsView.as_view(), name="evaluacion_details"),
    path('evaluacion/delete/<int:pk>/', EvaluacionDeleteView.as_view(), name="evaluacion_delete"),

]