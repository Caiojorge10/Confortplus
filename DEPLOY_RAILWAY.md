# Deploy do Confort Plus no Railway

Este guia fornece instruções detalhadas para fazer o deploy do Confort Plus na plataforma Railway.

## 📋 Pré-requisitos

1. Conta no [Railway](https://railway.app/)
2. Git instalado no computador
3. Railway CLI (opcional)
4. Projeto Confort Plus pronto para produção

## 🚀 Passo a Passo

### 1. Preparação do Projeto

#### Backend (Django)
1. Certifique-se de que o arquivo `requirements.txt` está atualizado:
```bash
cd backend
pip freeze > requirements.txt
```

2. Crie um arquivo `Procfile` na raiz do backend:
```
web: gunicorn confortplus.wsgi --log-file -
```

3. Adicione o `gunicorn` ao `requirements.txt`:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

4. Atualize as configurações de produção em `settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['*.railway.app']

# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE'),
        'USER': os.getenv('PGUSER'),
        'PASSWORD': os.getenv('PGPASSWORD'),
        'HOST': os.getenv('PGHOST'),
        'PORT': os.getenv('PGPORT'),
    }
}

# Configuração de arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
```

#### Frontend (React)
1. Atualize a URL da API no frontend:
```javascript
// src/config/api.js
const API_URL = process.env.REACT_APP_API_URL || 'https://sua-api.railway.app';
```

2. Gere o build de produção:
```bash
cd frontend
npm run build
```

### 2. Deploy no Railway

#### Backend (Django)

1. Acesse [Railway](https://railway.app/) e faça login
2. Clique em "New Project" → "Deploy from GitHub"
3. Selecione o repositório do seu projeto
4. Configure as variáveis de ambiente:
   - `SECRET_KEY`: Sua chave secreta do Django
   - `ALLOWED_HOSTS`: Domínio do Railway
   - `DATABASE_URL`: Será configurado automaticamente
   - `REACT_APP_API_URL`: URL do backend

5. Railway detectará automaticamente que é um projeto Django e configurará o build

#### Frontend (React)

1. Crie um novo serviço no mesmo projeto:
   - Clique em "New Service" → "Deploy from GitHub"
   - Selecione o repositório frontend
   - Configure o build command: `npm run build`
   - Configure o start command: `serve -s build`

2. Configure as variáveis de ambiente:
   - `REACT_APP_API_URL`: URL do backend
   - `NODE_ENV`: production

### 3. Configuração do Banco de Dados

1. No Railway, adicione um PostgreSQL:
   - Clique em "New Service" → "Database" → "PostgreSQL"
   - O Railway configurará automaticamente as variáveis de ambiente

2. Execute as migrações:
```bash
python manage.py migrate
```

3. Crie o superusuário:
```bash
python manage.py createsuperuser
```

### 4. Configuração de Domínio (Opcional)

1. No Railway, vá para as configurações do serviço
2. Na seção "Domains", você pode:
   - Usar o domínio fornecido pelo Railway
   - Configurar um domínio personalizado

### 5. Monitoramento

O Railway fornece:
- Logs em tempo real
- Métricas de uso
- Status do deploy
- Histórico de deploys

## 🔍 Verificação do Deploy

1. Acesse a URL fornecida pelo Railway
2. Verifique se:
   - Frontend carrega corretamente
   - Login funciona
   - Agendamentos podem ser criados
   - Vouchers são gerados

## ⚠️ Solução de Problemas

### Erros Comuns

1. **Erro de Conexão com Banco de Dados**
   - Verifique as variáveis de ambiente
   - Confirme se o serviço PostgreSQL está ativo

2. **Erro 500 no Backend**
   - Verifique os logs do Railway
   - Confirme as configurações do ALLOWED_HOSTS

3. **Frontend não Conecta com Backend**
   - Verifique a URL da API no frontend
   - Confirme se o CORS está configurado corretamente

### Comandos Úteis

```bash
# Ver logs do Railway
railway logs

# Executar comandos Django
railway run python manage.py migrate

# Reiniciar serviço
railway service restart
```

## 📝 Manutenção

1. **Atualizações**
   - Push para o GitHub inicia deploy automático
   - Monitore os logs após updates

2. **Backup**
   - Railway faz backup automático do banco
   - Exporte dados importantes periodicamente

3. **Monitoramento**
   - Configure alertas no Railway
   - Monitore uso de recursos

## 🤝 Suporte

Para problemas com o deploy, consulte:
- [Documentação do Railway](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- Suporte Confort Plus: suporte@confortplus.com.br 