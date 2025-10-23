from django.db import models
from .cliente import Cliente

class Veiculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="veiculos"
    )
    placa = models.CharField("placa", max_length=12)
    modelo = models.CharField("modelo", max_length=100, blank=True, null=True)
    ano = models.PositiveIntegerField("ano", blank=True, null=True)

    data_criacao = models.DateTimeField("data de criação", auto_now_add=True)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"{self.placa} — {self.modelo or 'Modelo não informado'}"
