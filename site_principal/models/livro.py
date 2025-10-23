from django.db import models
from .autor import Autor

class Livro(models.Model):
    id_livro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    ano_publicacao = models.IntegerField()
    editora = models.CharField(max_length=150)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    quantidade_exemplares = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.titulo} ({self.autor.nome})"
