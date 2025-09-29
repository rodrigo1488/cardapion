from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database import supabase
import hashlib
import uuid

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/', methods=['GET'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    # Só processa JSON se for POST
    if request.method != 'POST':
        return jsonify({"error": "Método não permitido"}), 405
    
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        if supabase:
            # Buscar usuário
            result = supabase.table('users_company').select('*').eq('email', email).execute()
            
            if not result.data:
                return jsonify({"error": "Email ou senha incorretos"}), 401
            
            user = result.data[0]
            
            # Verificar senha (em produção, usar hash adequado)
            if user['password'] != password:
                return jsonify({"error": "Email ou senha incorretos"}), 401
            
            # Buscar dados da empresa
            company_result = supabase.table('company').select('*').eq('id', user['id_company']).execute()
            company = company_result.data[0] if company_result.data else None
            
            # Criar sessão
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['company_id'] = user['id_company']
            session['company_name'] = company['name'] if company else 'Empresa'
            
            return jsonify({
                "message": "Login realizado com sucesso",
                "user": {
                    "id": user['id'],
                    "name": user['name'],
                    "email": user['email'],
                    "company_id": user['id_company'],
                    "company_name": company['name'] if company else 'Empresa'
                }
            }), 200
        else:
            # Modo de desenvolvimento - login de teste
            if email == "admin@teste.com" and password == "123456":
                session['user_id'] = 'test-user-id'
                session['user_name'] = 'Usuário Teste'
                session['user_email'] = email
                session['company_id'] = 'test-company-id'
                session['company_name'] = 'Empresa Teste'
                
                return jsonify({
                    "message": "Login realizado com sucesso (modo de desenvolvimento)",
                    "user": {
                        "id": 'test-user-id',
                        "name": 'Usuário Teste',
                        "email": email,
                        "company_id": 'test-company-id',
                        "company_name": 'Empresa Teste'
                    }
                }), 200
            else:
                return jsonify({"error": "Email ou senha incorretos. Use admin@teste.com / 123456 para teste"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'GET':
        return render_template('register_company.html')
    
    try:
        data = request.get_json()
        required_fields = ['name', 'email', 'contact', 'address', 'cnpj']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"O campo {field} é obrigatório"}), 400
        
        # Verificar se CNPJ já existe
        if supabase:
            existing_company = supabase.table('company').select('*').eq('cnpj', data.get('cnpj')).execute()
            if existing_company.data:
                return jsonify({"error": "CNPJ já cadastrado"}), 400
            
            # Verificar se email já existe
            existing_email = supabase.table('company').select('*').eq('email', data.get('email')).execute()
            if existing_email.data:
                return jsonify({"error": "Email já cadastrado"}), 400
        
        company_data = {
            "name": data.get('name'),
            "email": data.get('email'),
            "contact": data.get('contact'),
            "adress": data.get('address'),  # Note: campo no banco é 'adress'
            "cnpj": data.get('cnpj'),
            "status_acess": True
        }
        
        if supabase:
            result = supabase.table('company').insert(company_data).execute()
            if result.data:
                company_id = result.data[0]['id']
                return jsonify({
                    "message": "Empresa cadastrada com sucesso",
                    "company_id": company_id
                }), 201
            else:
                return jsonify({"error": "Erro ao cadastrar empresa"}), 500
        else:
            # Modo de desenvolvimento - simular cadastro
            return jsonify({
                "message": "Empresa cadastrada com sucesso (modo de desenvolvimento)",
                "company_id": "test-company-id"
            }), 201
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register_user.html')
    
    try:
        data = request.get_json()
        required_fields = ['name', 'email', 'password', 'id_company']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"O campo {field} é obrigatório"}), 400
        
        # Verificar se email já existe
        if supabase:
            existing_user = supabase.table('users_company').select('*').eq('email', data.get('email')).execute()
            if existing_user.data:
                return jsonify({"error": "Email já cadastrado"}), 400
        
        user_data = {
            "name": data.get('name'),
            "email": data.get('email'),
            "password": data.get('password'),  # Em produção, usar hash
            "id_company": data.get('id_company')
        }
        
        if supabase:
            result = supabase.table('users_company').insert(user_data).execute()
            if result.data:
                return jsonify({
                    "message": "Usuário criado com sucesso"
                }), 201
            else:
                return jsonify({"error": "Erro ao criar usuário"}), 500
        else:
            # Modo de desenvolvimento - simular criação
            return jsonify({
                "message": "Usuário criado com sucesso (modo de desenvolvimento)"
            }), 201
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    return render_template('dashboard.html')

@auth_bp.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    
    return render_template('settings.html', company_id=session.get('company_id', 'test-company-id'))

# Decorator para verificar autenticação
def login_required(f):
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function
