from django.contrib import admin
from .models import Cliente, Motorista, Agendamento
from django.contrib.auth.models import User

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')

@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cnh', 'ativo')
    search_fields = ('nome', 'email')
    list_filter = ('ativo',)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'cliente', 
        'origem', 
        'destino', 
        'data',
        'hora',
        'valor', 
        'status'
    )
    list_filter = ('status', 'data')
    search_fields = ('origem', 'destino', 'cliente__username')
    ordering = ('-data', '-hora')
