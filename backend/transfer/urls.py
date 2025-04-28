from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AgendamentoViewSet, 
    ClienteViewSet, 
    MotoristaViewSet, 
    get_user_me,
    PerfilViewSet
)
from . import auth
from . import views

router = DefaultRouter()
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')
router.register(r'clientes', ClienteViewSet)
router.register(r'motoristas', MotoristaViewSet)
router.register(r'perfil', PerfilViewSet, basename='perfil')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/registro/', auth.registro, name='registro'),
    path('auth/login/', auth.login, name='login'),
    path('usuarios/check-tipo/', views.check_user_type, name='check-user-type'),
    path('usuarios/me/', get_user_me, name='user-me'),
] 