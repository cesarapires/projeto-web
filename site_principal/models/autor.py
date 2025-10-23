from django.db import models

class Autor(models.Model):
    id_autor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    nacionalidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome
