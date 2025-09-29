# 🚀 Instruções de Uso - Cardápio Digital

## ✅ **Sistema Funcionando!**

A aplicação está rodando em `http://localhost:5000`

## 🔧 **Configuração Atual**

O sistema está configurado para funcionar em **modo de desenvolvimento** sem necessidade de banco de dados.

### **Credenciais de Teste:**
- **Email:** `admin@teste.com`
- **Senha:** `123456`

## 📱 **Como Testar o Sistema**

### 1. **Acesse a Aplicação**
Abra seu navegador e vá para: `http://localhost:5000`

### 2. **Teste o Login**
- Use as credenciais: `admin@teste.com` / `123456`
- Clique em "Entrar"
- Você será redirecionado para o dashboard

### 3. **Explore o Dashboard**
- Visualize as estatísticas
- Teste o menu lateral (clique no ícone de menu no mobile)
- Explore as diferentes seções

### 4. **Teste o Cadastro (Modo Desenvolvimento)**
- Clique em "Criar nova conta"
- Preencha os dados da empresa
- Preencha os dados do usuário
- O sistema simulará o cadastro

## 🎨 **Interface**

- **Design:** Neomorphism com Tailwind CSS
- **Responsivo:** Mobile-first
- **Cores:** Paleta laranja (#F97316) com cinzas neutros
- **Componentes:** Sombras suaves, transições animadas

## 🔄 **Para Usar com Banco Real**

1. **Configure o Supabase:**
   - Crie uma conta no [Supabase](https://supabase.com)
   - Crie um novo projeto
   - Execute o arquivo `cardapio.sql` no SQL Editor

2. **Configure o arquivo `.env`:**
   ```env
   SUPABASE_URL=sua_url_do_supabase
   SUPABASE_KEY=sua_chave_do_supabase
   SECRET_KEY=sua_chave_secreta_flask
   ```

3. **Reinicie a aplicação:**
   ```bash
   python app.py
   ```

## 📁 **Estrutura de Arquivos**

```
cardapion/
├── app.py                    # Aplicação principal
├── database.py              # Configuração do Supabase
├── requirements.txt         # Dependências
├── .env.example            # Exemplo de configuração
├── cardapio.sql           # Schema do banco
├── routes/                # Rotas da aplicação
│   ├── auth.py           # Autenticação
│   ├── company.py        # Empresas
│   └── users.py          # Usuários
└── templates/            # Templates HTML
    ├── base.html         # Template base
    ├── login.html        # Página de login
    ├── dashboard.html    # Dashboard
    └── components/       # Componentes reutilizáveis
```

## 🎯 **Funcionalidades Implementadas**

- ✅ Sistema de login/cadastro
- ✅ Dashboard responsivo
- ✅ Menu lateral com navegação
- ✅ Interface neomorphism
- ✅ Modo de desenvolvimento
- ✅ Validações de formulário
- ✅ Sessões de usuário

## 🚀 **Próximos Passos**

Para continuar o desenvolvimento, você pode implementar:

1. **Sistema de Cardápio**
   - CRUD de categorias
   - CRUD de produtos
   - Upload de imagens

2. **Sistema de Pedidos**
   - Criação de pedidos
   - Status de pedidos
   - Notificações em tempo real

3. **Sistema de Mesas**
   - Gerenciamento de mesas
   - Status das mesas
   - QR codes para mesas

4. **Relatórios**
   - Dashboard com gráficos
   - Relatórios de vendas
   - Estatísticas de produtos

## 🆘 **Problemas Comuns**

### **Erro de Conexão com Supabase**
- Verifique se o arquivo `.env` está configurado
- Confirme se as credenciais estão corretas
- O sistema funciona em modo de desenvolvimento sem banco

### **Página não carrega**
- Verifique se a aplicação está rodando: `python app.py`
- Confirme se a porta 5000 está livre
- Acesse `http://localhost:5000`

### **Erro de Dependências**
- Execute: `pip install -r requirements.txt`
- Verifique se o Python 3.8+ está instalado

## 📞 **Suporte**

Se encontrar problemas:
1. Verifique os logs no terminal
2. Confirme se todas as dependências estão instaladas
3. Teste com as credenciais de desenvolvimento

---

**🎉 Sistema pronto para uso e desenvolvimento!**
