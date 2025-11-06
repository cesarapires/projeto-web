from django.db import models
from .veiculo import Veiculo
from decimal import Decimal
from django.db.models import Sum


class OrdemServico(models.Model):
    STATUS_ABERTA = "aberta"
    STATUS_EM_ANDAMENTO = "em_andamento"
    STATUS_AGUARDANDO_APROVACAO = "aguardando_aprovacao"
    STATUS_FINALIZADA = "finalizada"
    STATUS_CANCELADA = "cancelada"

    STATUS_CHOICES = [
        (STATUS_ABERTA, "Aberta"),
        (STATUS_EM_ANDAMENTO, "Em andamento"),
        (STATUS_AGUARDANDO_APROVACAO, "Aguardando aprovação"),
        (STATUS_FINALIZADA, "Finalizada"),
        (STATUS_CANCELADA, "Cancelada"),
    ]

    id = models.BigAutoField(primary_key=True)
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.CASCADE, related_name="ordens_servico"
    )
    # por enquanto não adicionamos o funcionario
    status = models.CharField("status", max_length=32, choices=STATUS_CHOICES, default=STATUS_ABERTA)

    data_abertura = models.DateTimeField("data de abertura", auto_now_add=True)
    data_fechamento = models.DateTimeField("data de encerramento", blank=True, null=True)

    km_atendimento = models.PositiveIntegerField("km atendimento", blank=True, null=True)
    observacoes = models.TextField("observações", blank=True, null=True)
    valor_total = models.DecimalField("valor total", max_digits=10, decimal_places=2, default=Decimal("0.00"))

    data_criacao = models.DateTimeField("data de criação", auto_now_add=True)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        ordering = ["-data_abertura"]

    def __str__(self):
        return f"OS #{self.id} — {self.veiculo.placa} ({self.status})"

    def recalculate_valor_total(self):
        """Recalcula o valor_total como soma de serviços executados + peças utilizadas."""
        total_servicos = self.servicos_executados.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        total_pecas = self.pecas_utilizadas.aggregate(total=Sum('valor_total'))['total'] or Decimal('0.00')
        try:
            new_total = (Decimal(total_servicos) or Decimal('0.00')) + (Decimal(total_pecas) or Decimal('0.00'))
        except Exception:
            new_total = Decimal('0.00')
        # Salva apenas o campo valor_total para evitar sobrescrever timestamps desnecessariamente
        self.valor_total = new_total
        self.save(update_fields=['valor_total'])
