from django.db import models
from .emprestimo import Emprestimo
from .livro import Livro

class ItemEmprestimo(models.Model):
    STATUS_CHOICES = [
        ('emprestado', 'Emprestado'),
        ('devolvido', 'Devolvido'),
    ]

    id_item = models.AutoField(primary_key=True)
    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='emprestado')

    def __str__(self):
        return f"{self.livro.titulo} - {self.status}"
