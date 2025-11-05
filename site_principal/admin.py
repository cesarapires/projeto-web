from django.contrib import admin

from .models import  Servico, Veiculo, Cliente, Agendamento, OrdemServico

admin.site.register(Servico)
admin.site.register(Veiculo)
admin.site.register(Cliente)
admin.site.register(Agendamento)
admin.site.register(OrdemServico)

