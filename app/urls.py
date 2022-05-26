from unicodedata import name
from django.urls import path, re_path, include
from app.views.views_archivo import ArchivoCreateView, ArchivoListView
from app.views.views_evaluacion import EvaluacionDeleteView, EvaluacionDetailsView, EvaluacionListView, EvaluacionCreateView
from app.views.views_notificacion import NotificacionDeleteView, NotificacionListView, NotificacionCreateView
from app.views.views_puntaje import PuntajeCreateView, PuntajeListView

from .views import UsuariosListView,UsuarioCreateView,UsuarioDetailsView, UsuarioUpdateView,UsuarioDeleteView,UsuarioEditView, LoginView
from .forms import CambiarPassForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


app_name="app"

urlpatterns= [
    #USUARIOS
    path('usuarios/', UsuariosListView.as_view(), name="usuarios"),
    path('usuarios/create/', UsuarioCreateView.as_view(), name="create"),
    path('usuarios/details/<int:pk>/', UsuarioDetailsView.as_view(), name="details"),
    path('usuarios/update/<int:pk>/', UsuarioUpdateView.as_view(), name="update"),
    path('usuarios/delete/<int:pk>/', UsuarioDeleteView.as_view(), name="delete"),

    #NOTIFICACION
    path('notificacion/', NotificacionListView.as_view(), name="notificacion"),
    path('notificacion_create/', NotificacionCreateView.as_view(), name="crear_notificacion"),
    path('notificacion/delete/<int:pk>/', NotificacionDeleteView.as_view(), name="notificacion_delete"),

    #ARCHIVOS
    path('archivos/', ArchivoListView.as_view(), name="archivos"),
    path('archivo_create/', ArchivoCreateView.as_view(), name="crear_archivo"),

    #EVALUACION
    path('evaluacion/', EvaluacionListView.as_view(), name="evaluacion"),
    path('evaluacion_create/', EvaluacionCreateView.as_view(), name="crear_evaluacion"),
    path('evaluacion/details/<int:pk>/', EvaluacionDetailsView.as_view(), name="evaluacion_details"),
    path('evaluacion/delete/<int:pk>/', EvaluacionDeleteView.as_view(), name="evaluacion_delete"),

    #PUNTAJES
    path('puntaje/', PuntajeListView.as_view(), name="puntaje"),
    path('puntaje_create/', PuntajeCreateView.as_view(), name="crear_puntaje"),

#Evaluacion

    # autenticación
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LoginView.logout_user, name="logout"),


    # resetear password
    path('cambiar_clave/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        subject_template_name='registration/password_reset_subject.txt',
        email_template_name='registration/password_reset_email.html',), name="custom_password_reset"),

    path('enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ),name="custom_password_create_done"),

    path('cambiar_clave/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        form_class=CambiarPassForm
    ), name="custom_password_reset_confirm"),

    path('cambiar_clave_hecho/', auth_views.PasswordResetCompleteView.as_view(), name="custom_password_reset_complete"),

    ## crear password urls ##

    path('crear/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_create_confirm.html',
        success_url='/crear/done/',
        form_class=CambiarPassForm),name="custom_password_create_confirm"),

    path('crear/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_create_complete.html'),
        name="custom_password_create_complete"),



    #re_path('password_reset/',auth_views.PasswordResetView.as_view(
    #    template_name='registration/password_reset_form.html',
    #    email_template_name='registration/password_reset_email.html',
    #    subject_template_name='registration/password_reset_subject.txt',
    #    success_url = reverse_lazy('app:password_reset_done')
    #    ),name='password_reset'),
    #re_path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    #re_path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    #re_path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('usuarios/edit/<int:pk>/', UsuarioEditView.as_view(), name="edit")

]
