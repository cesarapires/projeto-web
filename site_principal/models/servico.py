from django.db import models

from .cliente import Agendamento

from decimal import Decimal

class Servico(models.Model):
    id = models.BigAutoField(primary_key=True)
    agendamento = models.ForeignKey(
        Agendamento, on_delete=models.CASCADE, related_name="servicos"
    )
    descricao = models.CharField("descrição", max_length=300)
    valor_estimado = models.DecimalField(
        "valor estimado", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    duracao_prevista = models.DurationField(
        "duração prevista", blank=True, null=True, help_text="Formato: HH:MM:SS"
    )
    realizado = models.BooleanField("realizado", default=False)

    data_criacao = models.DateTimeField("data de criação", auto_now_add=True)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"{self.descricao} — R$ {self.valor_estimado}"
