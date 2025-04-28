from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from .models import Cliente

@api_view(['POST'])
@permission_classes([AllowAny])
def registro(request):
    try:
        with transaction.atomic():
            data = request.data
            
            # Verifica se o email já existe
            if User.objects.filter(email=data['email']).exists():
                return Response({
                    'message': 'Este email já está em uso'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Cria o usuário
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['nome'].split()[0],
                last_name=' '.join(data['nome'].split()[1:]) if len(data['nome'].split()) > 1 else ''
            )
            
            # Cria o perfil do cliente
            cliente = Cliente.objects.create(
                user=user,
                nome=data['nome'],
                email=data['email'],
                telefone=data['telefone']
            )
            
            # Gera o token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'token': str(refresh.access_token),
                'user_id': user.id,
                'message': 'Conta criada com sucesso!'
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print("Erro no registro:", str(e))  # Para debug
        return Response({
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Tenta autenticar com email/username
        user = authenticate(username=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'user_id': user.id,
                'message': 'Login realizado com sucesso!'
            })
        else:
            return Response({
                'message': 'Credenciais inválidas'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except Exception as e:
        return Response({
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST) 