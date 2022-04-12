from unicodedata import name
from django.urls import path

from app.views.views_usuarios import UsuarioEditView
from .views import UsuariosListView,UsuarioCreateView,UsuarioDetailsView, UsuarioUpdateView,UsuarioDeleteView

app_name="app"

urlpatterns= [
    path('usuarios', UsuariosListView.as_view(), name="usuarios"),
    path('usuarios/create/', UsuarioCreateView.as_view(), name="create"),
    path('usuarios/details/<int:pk>/', UsuarioDetailsView.as_view(), name="details"),
    path('usuarios/update/<int:pk>/', UsuarioUpdateView.as_view(), name="update"),
    path('usuarios/delete/<int:pk>/', UsuarioDeleteView.as_view(), name="delete"),
    path('usuarios/edit/', UsuarioEditView.as_view(), name="edit")

]