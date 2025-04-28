from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Cliente, Motorista, Agendamento
from .serializers import ClienteSerializer, MotoristaSerializer, AgendamentoSerializer, UserSerializer, PerfilSerializer, VoucherSerializer, MotoristaSimpleSerializer
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

# Create your views here.

class IsClienteOrStaff(permissions.BasePermission):
    """
    Permissão customizada para permitir que clientes vejam seus próprios agendamentos
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Permite se for staff
        if request.user.is_staff:
            return True
        # Permite se for o cliente do agendamento
        try:
            cliente = request.user.cliente
            return obj.cliente == cliente
        except Cliente.DoesNotExist:
            return False

class IsMotoristaOrStaff(permissions.BasePermission):
    """
    Permissão customizada para motoristas
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(hasattr(request.user, 'motorista') or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        try:
            return obj.motorista == request.user.motorista
        except:
            return False

class AgendamentoViewSet(viewsets.ModelViewSet):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Agendamento.objects.all()
        
        if hasattr(user, 'motorista'):
            return Agendamento.objects.filter(motorista=user.motorista)
            
        if hasattr(user, 'cliente'):
            return Agendamento.objects.filter(cliente=user.cliente)
            
        return Agendamento.objects.none()

    def get_object(self):
        """Sobrescreve o método para adicionar logs de debug"""
        try:
            obj = super().get_object()
            return obj
        except Exception as e:
            print("Erro ao buscar agendamento:", str(e))
            print("User:", self.request.user)
            print("User type:", type(self.request.user))
            if hasattr(self.request.user, 'motorista'):
                print("Motorista:", self.request.user.motorista)
            raise

    def perform_create(self, serializer):
        """Adiciona o cliente automaticamente ao criar agendamento"""
        try:
            cliente = Cliente.objects.get(user=self.request.user)
            motorista = Motorista.objects.filter(ativo=True).first()
            
            if not motorista:
                raise serializers.ValidationError("Nenhum motorista disponível")

            serializer.save(
                cliente=cliente,
                motorista=motorista
            )
        except Cliente.DoesNotExist:
            raise serializers.ValidationError(
                "Usuário não tem um perfil de cliente associado. Por favor, crie um perfil de cliente primeiro."
            )

    def create(self, request):
        try:
            try:
                cliente = request.user.cliente
            except Cliente.DoesNotExist:
                return Response(
                    {'error': 'Usuário não tem um perfil de cliente associado'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Pega o motorista selecionado
            motorista_id = request.data.get('motorista')
            try:
                motorista = Motorista.objects.get(id=motorista_id, ativo=True)
            except Motorista.DoesNotExist:
                return Response(
                    {'error': 'Motorista não encontrado ou inativo'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            data_str = request.data.get('data')
            hora_str = request.data.get('hora')
            
            if not data_str or not hora_str:
                return Response(
                    {'error': 'Data e hora são obrigatórios'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                # Converte a string de data para objeto date
                data = datetime.strptime(data_str, "%Y-%m-%d").date()
                # Converte a string de hora para objeto time
                hora = datetime.strptime(hora_str, "%H:%M").time()
                # Combina data e hora para verificação de disponibilidade
                data_hora = datetime.combine(data, hora)
            except ValueError:
                return Response(
                    {'error': 'Formato de data ou hora inválido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verifica disponibilidade apenas do motorista selecionado
            if not motorista.esta_disponivel(data_hora):
                return Response(
                    {'error': 'Motorista não disponível neste horário'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Cria o agendamento
            agendamento = Agendamento(
                cliente=cliente,
                motorista=motorista,  # Usa o motorista selecionado
                nome_passageiro=request.data.get('nome_passageiro'),
                origem=request.data.get('origem'),
                destino=request.data.get('destino'),
                quantidade_adultos=int(request.data.get('quantidade_adultos', 1)),
                quantidade_criancas=int(request.data.get('quantidade_criancas', 0)),
                data=data,  # Usa o objeto date convertido
                hora=hora,  # Usa o objeto time convertido
                numero_voo=request.data.get('numero_voo'),
                tipo_servico=request.data.get('tipo_servico', 'TRANSFER'),
                telefone_contato=request.data.get('telefone_contato'),
                forma_pagamento=request.data.get('forma_pagamento', 'PIX'),
                valor=float(request.data.get('valor', 0)),
                valor_adiantamento=float(request.data.get('valor_adiantamento', 0)),
                status='PENDENTE'
            )
            
            agendamento.save()
            serializer = self.get_serializer(agendamento)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def gerar_voucher(self, request, pk=None):
        """Gera um voucher para o agendamento"""
        try:
            agendamento = self.get_object()
            serializer = VoucherSerializer(agendamento)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            novo_status = request.data.get('status')
            
            # Se estiver atualizando apenas o status
            if len(request.data) == 1 and 'status' in request.data:
                # Validação de transição de status
                transicoes_validas = {
                    'PENDENTE': ['CONFIRMADO', 'CANCELADO'],
                    'CONFIRMADO': ['CONCLUIDO', 'CANCELADO'],
                    'CONCLUIDO': [],
                    'CANCELADO': []
                }
                
                if novo_status not in transicoes_validas.get(instance.status, []):
                    error_msg = f'Transição de status inválida de {instance.status} para {novo_status}'
                    return Response(
                        {'error': error_msg},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                instance.status = novo_status
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            
            return super().update(request, *args, **kwargs)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False, 
        methods=['get']
    )
    def meus_agendamentos(self, request):
        """Endpoint para clientes verem seus agendamentos"""
        try:
            if not hasattr(request.user, 'cliente'):
                return Response(
                    {'error': 'Usuário não é um cliente'},
                    status=status.HTTP_403_FORBIDDEN
                )

            agendamentos = (
                Agendamento.objects
                .filter(cliente=request.user.cliente)
                .select_related('motorista')
                .order_by('-data', '-hora')  # Corrigido: usando os novos campos
            )
            
            serializer = self.get_serializer(agendamentos, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False, 
        methods=['get'],
        permission_classes=[IsMotoristaOrStaff]
    )
    def agendamentos_motorista(self, request):
        """Endpoint específico para motoristas"""
        try:
            if not hasattr(request.user, 'motorista'):
                return Response(
                    {'error': 'Usuário não é um motorista'},
                    status=status.HTTP_403_FORBIDDEN
                )

            agendamentos = (
                Agendamento.objects
                .filter(motorista=request.user.motorista)
                .order_by('-data', '-hora')  # Corrigido: usando os novos campos
            )
            
            serializer = self.get_serializer(agendamentos, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def motoristas_ativos(self, request):
        """Retorna lista de motoristas ativos"""
        try:
            motoristas = Motorista.objects.filter(ativo=True)
            serializer = MotoristaSimpleSerializer(motoristas, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            # Verifica se o usuário já é motorista
            if hasattr(request.user, 'motorista'):
                return Response(
                    {'error': 'Usuário já é um motorista'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Cria o motorista
            data = request.data.copy()
            data['user'] = request.user.id
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_type(request):
    """Verifica se o usuário é motorista e retorna suas informações"""
    try:
        is_motorista = hasattr(request.user, 'motorista')
        response_data = {'is_motorista': is_motorista}
        
        if is_motorista:
            motorista = request.user.motorista
            response_data.update({
                'motorista_id': motorista.id,
                'nome': motorista.nome,
                'ativo': motorista.ativo
            })
        
        return Response(response_data)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_me(request):
    """Endpoint para retornar dados do usuário logado"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class PerfilViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cliente.objects.filter(user=self.request.user)

    def get_object(self):
        try:
            return Cliente.objects.get(user=self.request.user)
        except Cliente.DoesNotExist:
            # Cria um perfil padrão se não existir
            return Cliente.objects.create(
                user=self.request.user,
                nome=self.request.user.username,
                email=self.request.user.email,
                telefone=""
            )

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            # Atualiza também os dados do usuário
            user = instance.user
            if 'email' in request.data:
                user.email = request.data['email']
                user.save()

            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
