from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.conf import settings
from datetime import datetime

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nome

class Motorista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='motorista', null=True)
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    cnh = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)
    
    def esta_disponivel(self, data_hora):
        from django.utils import timezone
        
        # Verifica agendamentos próximos
        agendamentos = self.agendamento_set.filter(
            status__in=['PENDENTE', 'CONFIRMADO']
        ).order_by('data', 'hora')
        
        # Tempo mínimo entre agendamentos (1 hora e 30 minutos)
        intervalo_minimo = timedelta(hours=1, minutes=30)
        
        for agendamento in agendamentos:
            # Combina data e hora do agendamento
            agendamento_datetime = datetime.combine(
                agendamento.data, 
                agendamento.hora
            )
            
            # Verifica se o novo horário está muito próximo de um agendamento existente
            inicio_janela = agendamento_datetime - intervalo_minimo
            fim_janela = agendamento_datetime + intervalo_minimo
            
            if inicio_janela <= data_hora <= fim_janela:
                return False
        
        return True
    
    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
        ('CONCLUIDO', 'Concluído'),
    ]

    TIPO_SERVICO_CHOICES = [
        ('TRANSFER', 'Transfer'),
        ('PASSEIO', 'Passeio'),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ('CREDITO', 'Cartão de Crédito'),
        ('DEBITO', 'Cartão de Débito'),
        ('BOLETO', 'Boleto'),
        ('PIX', 'PIX'),
        ('DINHEIRO', 'Dinheiro')
    ]

    VALORES_SERVICO = {
        'TRANSFER': {
            'valor_base_adulto': 150.00,
            'valor_base_crianca': 75.00,
        },
        'PASSEIO': {
            'valor_base_adulto': 200.00,
            'valor_base_crianca': 100.00,
        }
    }

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT)
    nome_passageiro = models.CharField(max_length=255)
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    quantidade_adultos = models.IntegerField(default=1)
    quantidade_criancas = models.IntegerField(default=0)
    data = models.DateField()
    hora = models.TimeField()
    numero_voo = models.CharField(max_length=20, blank=True, null=True)
    tipo_servico = models.CharField(
        max_length=20,
        choices=TIPO_SERVICO_CHOICES,
        default='TRANSFER'
    )
    telefone_contato = models.CharField(max_length=20)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        default='PIX'
    )
    valor_adiantamento = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data', '-hora']

    def calcular_valor_total(self):
        valores = self.VALORES_SERVICO[self.tipo_servico]
        valor_adultos = valores['valor_base_adulto'] * self.quantidade_adultos
        valor_criancas = valores['valor_base_crianca'] * self.quantidade_criancas
        return valor_adultos + valor_criancas

    def save(self, *args, **kwargs):
        if not self.valor:  # Se o valor não foi definido
            self.valor = self.calcular_valor_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Agendamento {self.id} - {self.nome_passageiro}"
