from django.contrib import admin

from .models import  Livro, Autor, Cliente, Emprestimo, ItemEmprestimo, Usuario

admin.site.register(Livro)
admin.site.register(Autor)
admin.site.register(Cliente)
admin.site.register(Emprestimo)
admin.site.register(ItemEmprestimo)
admin.site.register(Usuario)

