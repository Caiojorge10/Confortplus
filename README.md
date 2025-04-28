# 🚗 Confort Plus - Sistema de Agendamento de Transfers

Sistema web para gerenciamento de transfers e geração de vouchers de viagem.

## 📋 Sobre o Projeto

O Confort Plus é uma solução completa para empresas de transfer que precisam gerenciar agendamentos, motoristas e gerar vouchers profissionais para seus clientes. O sistema oferece uma interface intuitiva e responsiva, permitindo o acesso tanto via desktop quanto dispositivos móveis.

## ✨ Principais Funcionalidades

### 📱 Área do Cliente
- Agendamento de transfers
- Visualização de histórico de viagens
- Download de vouchers
- Gestão de perfil

### 🚘 Área do Motorista
- Visualização de agenda
- Confirmação de serviços
- Geração de ordem de serviço
- Status em tempo real

### 👨‍💼 Painel Administrativo
- Gestão completa de usuários
- Controle de agendamentos
- Relatórios e estatísticas
- Configurações do sistema

## 🛠 Tecnologias Utilizadas

### Frontend
- React.js
- Material-UI
- React Router
- Axios
- html2canvas
- jsPDF

### Backend
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Gunicorn

## 🗂 Estrutura do Projeto

```
confortplus/
├── backend/
│   ├── confortplus/
│   ├── api/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── README.md
└── DEPLOY_RAILWAY.md
```

## 🚀 Configuração do Ambiente de Desenvolvimento

### Pré-requisitos
- Python 3.8+
- Node.js 14+
- PostgreSQL
- Git

### Backend (Django)

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/confortplus.git
cd confortplus/backend
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

### Frontend (React)

1. Navegue até a pasta do frontend:
```bash
cd ../frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. Inicie o servidor de desenvolvimento:
```bash
npm start
```

## 👤 Usuário Padrão

Após a configuração inicial, um usuário administrador padrão é criado:

- **Usuário**: admin
- **Email**: admin@confortplus.com.br
- **Senha**: admin123

⚠️ Recomendamos alterar essas credenciais em produção.

## 📱 Responsividade

O sistema foi desenvolvido com foco em responsividade, adaptando-se a diferentes tamanhos de tela:
- Desktop
- Tablets
- Smartphones

## 🔒 Segurança

- Autenticação JWT
- Proteção contra CSRF
- Validação de dados
- Sanitização de inputs
- Rate limiting
- CORS configurado

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Suporte

Para suporte e dúvidas:
- Email: suporte@confortplus.com.br
- Documentação: [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)

## 🌟 Contribuindo

1. Faça o fork do projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ✨ Agradecimentos

Agradecemos a todos que contribuíram para tornar este projeto possível! 