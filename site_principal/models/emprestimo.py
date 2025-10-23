from django.db import models
from .cliente import Cliente

class Emprestimo(models.Model):
    id_emprestimo = models.AutoField(primary_key=True)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Empréstimo {self.id_emprestimo} - {self.cliente.nome}"
