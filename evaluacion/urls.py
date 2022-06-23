from evaluacion.views import EvaluacionDeleteView, EvaluacionDetailsView, EvaluacionEditView, EvaluacionListView, EvaluacionCreateView, PuntajeEvCreateView, PuntajeEvEditView, PuntajesEvListView, deletePuntajeEv, updatePuntaje, usuariosEvaluacionAPI
from django.urls import path

app_name="evaluacion"

urlpatterns= [

    #EVALUACION
    path('evaluacion/', EvaluacionListView.as_view(), name="evaluaciones"),
    path('evaluacion/crear/', EvaluacionCreateView.as_view(), name="crear_evaluacion"),
    path('evaluacion/details/<int:pk>/', EvaluacionDetailsView.as_view(), name="evaluacion_details"),
    path('evaluacion/eliminar/<int:pk>/', EvaluacionDeleteView.as_view(), name="evaluacion_delete"),
    path('evaluacion/editar/<int:pk>/', EvaluacionEditView.as_view(), name="evaluacion_edit"),
    path('evaluacionPuntajesAPI/<int:pk>/', usuariosEvaluacionAPI),
    path('updatePuntajeEv/', updatePuntaje),

    #Puntajes para cada tipo de actividad
    path('configuracion/puntajes-evaluacion/', PuntajesEvListView.as_view(), name="evaluacion_puntajes"),
    path('configuracion/puntajes-evaluacion/crear/', PuntajeEvCreateView.as_view(), name="crear_puntaje_evaluacion"),
    path('configuracion/puntajes-evaluacion/editar/<int:pk>/', PuntajeEvEditView.as_view(), name="editar_puntaje_evaluacion"),
    path('configuracion/puntajes-evaluacion/eliminar/<int:pk>/', deletePuntajeEv, name="delete_puntaje_evaluacion"),
]