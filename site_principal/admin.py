from django.contrib import admin

from .models import  Servico, Veiculo, Cliente, Agendamento, OrdemServico, Peca

admin.site.register(Servico)
admin.site.register(Veiculo)
admin.site.register(Cliente)
admin.site.register(Agendamento)
admin.site.register(OrdemServico)
admin.site.register(Peca)

