from django.db import models
from .cliente import Veiculo
from django.utils import timezone

class Agendamento(models.Model):
    STATUS_PENDENTE = "P"
    STATUS_EM_ANDAMENTO = "E"
    STATUS_CONCLUIDO = "C"
    STATUS_CANCELADO = "X"

    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_EM_ANDAMENTO, "Em andamento"),
        (STATUS_CONCLUIDO, "Concluído"),
        (STATUS_CANCELADO, "Cancelado"),
    ]

    id = models.BigAutoField(primary_key=True)
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.CASCADE, related_name="agendamentos"
    )
    # usar DateTimeField para data+hora juntos (mais prático)
    data_hora_agendada = models.DateTimeField("data e hora agendada")
    status = models.CharField(
        "status", max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDENTE
    )

    observacoes = models.TextField("observações", blank=True, null=True)

    data_criacao = models.DateTimeField("data de criação", auto_now_add=True)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ["-data_hora_agendada"]

    def __str__(self):
        return f"Agendamento #{self.id} — {self.veiculo.placa} @ {self.data_hora_agendada}"
    
    @property
    def is_future(self):
        return self.data_hora_agendada > timezone.now()
