from django.db import models

class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField("nome", max_length=150)
    telefone = models.CharField("telefone", max_length=20, blank=True, null=True)
    email = models.EmailField("email", unique=True)

    data_criacao = models.DateTimeField("data de criação", auto_now_add=True)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} <{self.email}>"
