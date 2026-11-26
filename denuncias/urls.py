from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.nova_denuncia, name='nova_denuncia'),
    path('confirmacao/<str:protocolo>/', views.confirmacao_denuncia, name='confirmacao_denuncia'),
    path('consultar/', views.consultar_status, name='consultar_status'),
    path('login/', auth_views.LoginView.as_view(template_name='denuncias/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('painel/', views.lista_denuncias, name='lista_denuncias'),
    path('painel/denuncia/<int:pk>/', views.detalhe_denuncia, name='detalhe_denuncia'),
]
