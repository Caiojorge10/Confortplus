from rest_framework import serializers
from .models import Cliente, Motorista, Agendamento
from django.contrib.auth import get_user_model

User = get_user_model()

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'telefone']

class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = ['id', 'nome', 'email', 'telefone', 'cnh', 'ativo']

class MotoristaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = ['id', 'nome']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class AgendamentoSerializer(serializers.ModelSerializer):
    motorista = MotoristaSimpleSerializer(read_only=True)
    cliente = ClienteSerializer(read_only=True)
    data_formatada = serializers.SerializerMethodField()
    hora_formatada = serializers.SerializerMethodField()
    
    class Meta:
        model = Agendamento
        fields = [
            'id', 
            'cliente', 
            'motorista',
            'nome_passageiro',
            'origem', 
            'destino',
            'quantidade_adultos',
            'quantidade_criancas', 
            'data',
            'hora',
            'data_formatada',
            'hora_formatada',
            'numero_voo',
            'tipo_servico',
            'telefone_contato',
            'forma_pagamento',
            'valor',
            'valor_adiantamento',
            'status'
        ]
        read_only_fields = ['cliente', 'motorista']

    def get_data_formatada(self, obj):
        return obj.data.strftime('%Y-%m-%d') if obj.data else None

    def get_hora_formatada(self, obj):
        return obj.hora.strftime('%H:%M') if obj.hora else None

    def create(self, validated_data):
        # Pega o primeiro motorista disponível (ou um específico se você preferir)
        motorista = Motorista.objects.filter(ativo=True).first()
        if not motorista:
            raise serializers.ValidationError("Nenhum motorista disponível")
            
        validated_data['motorista'] = motorista
        return super().create(validated_data)

class PerfilSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'telefone', 'username']

class VoucherSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome')
    motorista_nome = serializers.CharField(source='motorista.nome')
    valor_saldo = serializers.SerializerMethodField()
    forma_pagamento_display = serializers.SerializerMethodField()
    data_formatada = serializers.SerializerMethodField()
    hora_formatada = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        fields = [
            'id',
            'cliente_nome',
            'motorista_nome',
            'nome_passageiro',
            'origem',
            'destino',
            'quantidade_adultos',
            'quantidade_criancas',
            'data_formatada',
            'hora_formatada',
            'numero_voo',
            'tipo_servico',
            'telefone_contato',
            'forma_pagamento',
            'forma_pagamento_display',
            'valor',
            'valor_adiantamento',
            'valor_saldo',
            'status'
        ]

    def get_valor_saldo(self, obj):
        return float(obj.valor) - float(obj.valor_adiantamento)

    def get_forma_pagamento_display(self, obj):
        return obj.get_forma_pagamento_display()

    def get_data_formatada(self, obj):
        return obj.data.strftime('%d/%m/%Y') if obj.data else None

    def get_hora_formatada(self, obj):
        return obj.hora.strftime('%H:%M') if obj.hora else None 