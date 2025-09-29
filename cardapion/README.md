# Cardápio Digital - Sistema SaaS Multiempresarial

Sistema de cardápio digital para restaurantes com funcionalidades de delivery e pedidos locais.

## 🚀 Funcionalidades

- **Multiempresarial**: Cada empresa tem seu próprio ambiente isolado
- **Autenticação**: Sistema de login com cadastro de empresa e usuário
- **Dashboard**: Painel administrativo com estatísticas em tempo real
- **Pedidos**: Suporte a pedidos delivery e locais (mesa)
- **Interface Responsiva**: Design mobile-first com Tailwind CSS
- **Neomorphism**: Interface moderna com efeitos de neomorphism

## 🛠️ Tecnologias

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, Alpine.js
- **Banco de Dados**: Supabase (PostgreSQL)
- **Autenticação**: Sessões Flask

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Supabase
- Git

## 🔧 Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd cardapion
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase
SECRET_KEY=sua_chave_secreta_flask
```

4. **Execute o banco de dados**
Execute o arquivo `cardapio.sql` no seu banco Supabase.

5. **Execute a aplicação**
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 📱 Como Usar

### 1. Cadastro de Empresa
- Acesse `/login`
- Clique em "Criar nova conta"
- Preencha os dados da empresa
- Confirme o cadastro

### 2. Cadastro do Primeiro Usuário
- Após cadastrar a empresa, você será redirecionado
- Preencha os dados do usuário administrador
- Crie uma senha segura
- Confirme o cadastro

### 3. Login
- Use o email e senha criados
- Acesse o dashboard

### 4. Dashboard
- Visualize estatísticas em tempo real
- Gerencie pedidos ativos
- Monitore status das mesas
- Acesse ações rápidas

## 🎨 Design System

### Paleta de Cores
- **Fundo**: #F5F5F5 (Cinza claro)
- **Cartões**: #FFFFFF (Branco)
- **Primária**: #F97316 (Laranja)
- **Texto**: #333333 (Cinza escuro)

### Componentes
- **Neomorphism**: Sombras suaves para profundidade
- **Responsivo**: Mobile-first design
- **Transições**: Animações suaves com Tailwind

## 📁 Estrutura do Projeto

```
cardapion/
├── app.py                 # Aplicação principal
├── database.py           # Configuração do Supabase
├── requirements.txt      # Dependências Python
├── cardapio.sql         # Schema do banco de dados
├── routes/              # Blueprints do Flask
│   ├── auth.py         # Autenticação
│   ├── company.py      # Empresas
│   └── users.py        # Usuários
└── templates/          # Templates HTML
    ├── base.html       # Template base
    ├── base_dashboard.html # Template com sidebar
    ├── login.html      # Página de login
    ├── register_company.html # Cadastro empresa
    ├── register_user.html    # Cadastro usuário
    ├── dashboard.html  # Dashboard principal
    └── components/
        └── sidebar.html # Menu lateral
```

## 🔐 Segurança

- Senhas devem ser hasheadas em produção
- Use HTTPS em produção
- Configure SECRET_KEY adequadamente
- Implemente rate limiting para APIs

## 🚀 Próximos Passos

- [ ] Implementar hash de senhas
- [ ] Adicionar validação de CNPJ
- [ ] Criar sistema de permissões
- [ ] Implementar notificações em tempo real
- [ ] Adicionar testes automatizados
- [ ] Configurar CI/CD

## 📞 Suporte

Para dúvidas ou sugestões, entre em contato através dos issues do repositório.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
