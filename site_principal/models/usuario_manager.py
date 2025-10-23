from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, cliente, senha=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um email')
        email = self.normalize_email(email)
        usuario = self.model(email=email, cliente=cliente, **extra_fields)
        usuario.set_password(senha)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, cliente, senha=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, cliente, senha, **extra_fields)
