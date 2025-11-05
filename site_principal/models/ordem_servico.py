from django.db import models
from .veiculo import Veiculo
from decimal import Decimal


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
