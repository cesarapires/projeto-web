from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .cliente import Cliente
from .usuario_manager import UsuarioManager  # importando o manager

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    ultimo_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cliente']

    def __str__(self):
        return self.email
