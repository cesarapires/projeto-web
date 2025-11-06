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
    path('dashboard/orcamentos/<int:pk>/detail/', views.cliente_orcamento_detail, name='cliente_orcamento_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/orcamentos/novo/', views.admin_orcamento_create, name='admin_orcamento_create'),
    path('dashboard/admin/orcamentos/<int:pk>/', views.admin_orcamento_detail, name='admin_orcamento_detail'),
    path('dashboard/admin/orcamentos/<int:pk>/editar/', views.admin_orcamento_edit, name='admin_orcamento_edit'),
    path('dashboard/admin/orcamentos/<int:pk>/excluir/', views.admin_orcamento_delete, name='admin_orcamento_delete'),
    # Peças (admin)
    path('dashboard/admin/pecas/', views.peca_list, name='peca_list'),
    path('dashboard/admin/pecas/novo/', views.peca_create, name='peca_create'),
    path('dashboard/admin/pecas/<int:pk>/editar/', views.peca_edit, name='peca_edit'),
    path('dashboard/admin/pecas/<int:pk>/excluir/', views.peca_delete, name='peca_delete'),
    # Serviços executados (dentro de uma ordem)
    path('dashboard/admin/orcamentos/<int:ordem_pk>/servicos/novo/', views.servico_create, name='servico_create'),
    path('dashboard/admin/orcamentos/<int:ordem_pk>/servicos/<int:pk>/editar/', views.servico_edit, name='servico_edit'),
    path('dashboard/admin/orcamentos/<int:ordem_pk>/servicos/<int:pk>/excluir/', views.servico_delete, name='servico_delete'),
]
