from django.db import models
from decimal import Decimal
from .ordem_servico import OrdemServico


class ServicoExecutado(models.Model):
    id = models.BigAutoField(primary_key=True)
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='servicos_executados')
    descricao = models.CharField('descrição', max_length=255)
    funcionario_id = models.BigIntegerField('ID do funcionário', null=True, blank=True)
    valor = models.DecimalField('valor', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    duracao_estimada_horas = models.DecimalField('duração estimada (h)', max_digits=4, decimal_places=2, null=True, blank=True)
    data_execucao = models.DateTimeField('data de execução', null=True, blank=True)

    criado_em = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Serviço Executado'
        verbose_name_plural = 'Serviços Executados'
        ordering = ['-criado_em']

    def __str__(self):
        return f"Serviço #{self.id} — {self.descricao[:40]}"
