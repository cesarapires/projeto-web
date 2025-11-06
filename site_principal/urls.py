from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.NonAdminLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/veiculos/novo/', views.veiculo_create, name='veiculo_create'),
    path('dashboard/veiculos/<int:pk>/editar/', views.veiculo_edit, name='veiculo_edit'),
    path('dashboard/veiculos/<int:pk>/excluir/', views.veiculo_delete, name='veiculo_delete'),
    path('dashboard/orcamentos/aguardando/', views.orcamentos_aguardando, name='orcamentos_aguardando'),
    path('dashboard/orcamentos/outros/', views.orcamentos_outros, name='orcamentos_outros'),
    path('dashboard/orcamentos/<int:pk>/aprovar/', views.aprovar_orcamento, name='aprovar_orcamento'),
    path('logout/', views.logout_view, name='logout'),
]
