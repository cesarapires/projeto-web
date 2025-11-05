from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.NonAdminLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
]
