from unicodedata import name
from django.urls import path, re_path, include
from app.views.views_archivo import ArchivoCreateView, ArchivoCreateView2, ArchivoDeleteView, ArchivoListView
from app.views.views_notificacion import NotificacionDeleteView, NotificacionDetails, NotificacionEditView, NotificacionListView, NotificacionCreateView

from app.views.views_tipo_actividad import TipoActividadCreateView, TipoActividadDeleteView, TipoActividadEditView, TipoActividadListView
from app.views.views_usuarios import UserChangePasswordView, deleteUser
from app.views.views_tipo_actividad import PuntajeCreateView, PuntajeEditView, TipoActividadCreateView, TipoActividadDetailsView, TipoActividadEditView, TipoActividadListView, delete, deletePuntaje


from .views import UsuariosListView,UsuarioCreateView,UsuarioDetailsView, UsuarioDeleteView,UsuarioEditView, LoginView
from .forms import CambiarPassForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from app import views


app_name="app"

urlpatterns= [

    #USUARIOS
    path('usuarios/', UsuariosListView.as_view(), name="usuarios"),
    path('usuarios/create/', UsuarioCreateView.as_view(), name="create"),
    path('usuarios/details/<int:pk>/', UsuarioDetailsView.as_view(), name="details"),
    path('usuarios/edit/<int:pk>/', UsuarioEditView.as_view(), name="edit"),
    path('usuarios/delete/<int:pk>/', deleteUser, name="delete"),
    path('usuarios/change_password/', UserChangePasswordView.as_view(), name="user_change_password"),

    #NOTIFICACION
    path('notificacion/', NotificacionListView.as_view(), name="notificacion"),
    path('notificacion_create/', NotificacionCreateView.as_view(), name="crear_notificacion"),
    path('notificacion/delete/<int:pk>/', NotificacionDeleteView.as_view(), name="notificacion_delete"),
    path('notificacion/edit/<int:pk>/', NotificacionEditView.as_view(), name="notificacion_edit"),
    path('notificacion/ver/<int:pk>/', NotificacionDetails.as_view(), name="notificacion_details"),
    
    #ARCHIVOS
    path('archivos/', ArchivoListView.as_view(), name="archivo"),
    path('archivo/subir/', ArchivoCreateView.as_view(), name="subir_archivo"),
    path('archivo/delete/<int:pk>/', ArchivoDeleteView.as_view(), name="archivo_delete"),

    #TIPO ACTIVIDAD
    path('configuracion/tipo_actividad/', TipoActividadListView.as_view(), name="list_tipo_actividad"),
    path('configuracion/tipo_actividad/create/', TipoActividadCreateView.as_view(), name="crear_tipo_actividad"),
    path('configuracion/tipo_actividad/delete/<int:pk>/', delete, name="delete_tipo_actividad"),
    path('configuracion/tipo_actividad/edit/<int:pk>/', TipoActividadEditView.as_view(), name="edit_tipo_actividad"),

    #Puntajes para cada tipo de actividad
    path('configuracion/tipo_actividad/puntajes/<int:pk>/', TipoActividadDetailsView.as_view(), name="tipo_actividad_puntajes"),
    path('configuracion/tipo_actividad/puntajes/crear/<int:tipo_id>', PuntajeCreateView.as_view(), name="crear_puntaje"),
    path('configuracion/tipo_actividad/puntajes/editar/<int:tipo_id>/<int:pk>/', PuntajeEditView.as_view(), name="editar_puntaje"),
    path('configuracion/puntajes/eliminar/<int:pk>/', deletePuntaje, name="delete_puntaje"),



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

]


    #re_path('password_reset/',auth_views.PasswordResetView.as_view(
    #    template_name='registration/password_reset_form.html',
    #    email_template_name='registration/password_reset_email.html',
    #    subject_template_name='registration/password_reset_subject.txt',
    #    success_url = reverse_lazy('app:password_reset_done')
    #    ),name='password_reset'),
    #re_path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    #re_path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    #re_path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),


