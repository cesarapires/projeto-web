from django.db import models
from decimal import Decimal
from .ordem_servico import OrdemServico
from .peca import Peca


class PecaUtilizada(models.Model):
    id = models.BigAutoField(primary_key=True)
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='pecas_utilizadas')
    peca = models.ForeignKey(Peca, on_delete=models.PROTECT, related_name='usos')
    quantidade = models.IntegerField('quantidade', default=1)
    valor_unitario = models.DecimalField('valor unitário', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_total = models.DecimalField('valor total', max_digits=10, decimal_places=2, default=Decimal('0.00'))

    criado_em = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Peça Utilizada'
        verbose_name_plural = 'Peças Utilizadas'
        ordering = ['-criado_em']

    def __str__(self):
        return f"Peça utilizada #{self.id} — {self.peca.nome} x{self.quantidade}"

    def save(self, *args, **kwargs):
        # calcula valor_total automaticamente
        if self.valor_unitario is None:
            self.valor_unitario = self.peca.preco_unitario if self.peca else Decimal('0.00')
        try:
            self.valor_total = (Decimal(self.quantidade) * Decimal(self.valor_unitario))
        except Exception:
            self.valor_total = Decimal('0.00')
        super().save(*args, **kwargs)
