from django.db import models
from decimal import Decimal


class Peca(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField('nome', max_length=100)
    codigo = models.CharField('código', max_length=50, blank=True)
    fabricante = models.CharField('fabricante', max_length=100, blank=True)
    preco_unitario = models.DecimalField('preço unitário', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    estoque_atual = models.IntegerField('estoque atual', default=0)
    criado_em = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.nome} ({self.codigo})" if self.codigo else self.nome
