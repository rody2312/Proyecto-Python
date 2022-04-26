from unicodedata import name
from django.urls import path, re_path, include

from app.views.views_notificacion import NotificacionListView, NotificacionCreateView

from .views import UsuariosListView,UsuarioCreateView,UsuarioDetailsView, UsuarioUpdateView,UsuarioDeleteView,UsuarioEditView, LoginView #NotificacionView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


app_name="app"

urlpatterns= [
    path('usuarios/', UsuariosListView.as_view(), name="usuarios"),
    path('usuarios/create/', UsuarioCreateView.as_view(), name="create"),
    path('usuarios/details/<int:pk>/', UsuarioDetailsView.as_view(), name="details"),
    path('usuarios/update/<int:pk>/', UsuarioUpdateView.as_view(), name="update"),
    path('usuarios/delete/<int:pk>/', UsuarioDeleteView.as_view(), name="delete"),
    path('notificacion/', NotificacionListView.as_view(), name="notificacion"),
    path('notificacion_create/', NotificacionCreateView.as_view(), name="crear notificacion"),

    # autenticación
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LoginView.logout_user, name="logout"),


    ## crear password urls ##
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        subject_template_name='registration/password_reset_subject.txt',
        email_template_name='registration/password_reset_email.html',
        success_url='done',), name="password_reset"),

    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'),name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/'),name="password_reset_confirm"),

    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name="password_reset_complete"),



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
