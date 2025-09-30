import re
from flask import Blueprint, request, jsonify, session
from database import supabase

company_bp = Blueprint('company_bp', "__name__")

@company_bp.route("/create_company", methods =["POST"])
def create_company():
    data = request.get_json()
    
    required_fields = ['name', 'email', 'contact', 'adress', 'cnpj']

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"o campo {field} é obrigatorio"}) 

    company_data ={
        "name": data.get("name"),
        "email": data.get("email"),
        "contact": data.get("contact"),
        "adress": data.get("adress"),
        "cnpj": data.get("cnpj")

    }

    if supabase:
        result = supabase.table("company").insert(company_data).execute()
        if result.data:
            return jsonify({"message":"cadastro realizado com sucesso, vamos criar o primeiro usuario"}),201
        else:
            return jsonify({"error": "erro ao realizar o cadastro da empresa, tente novamente mais tarde"}),500

# API - Buscar dados da empresa
@company_bp.route('/api/company/<company_id>')
def get_company(company_id):
    try:
        if supabase:
            result = supabase.table('company').select('*').eq('id', company_id).execute()
            if not result.data:
                return jsonify({"error": "Empresa não encontrada"}), 404
            return jsonify({"company": result.data[0]})
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Atualizar dados da empresa
@company_bp.route('/api/company/<company_id>/update', methods=['PUT'])
def update_company(company_id):
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'contact', 'cnpj', 'address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400

        update_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'contact': data.get('contact'),
            'cnpj': data.get('cnpj'),
            'adress': data.get('address')  # Note: campo no banco é 'adress'
        }

        if supabase:
            result = supabase.table('company').update(update_data).eq('id', company_id).execute()
            if result.data:
                return jsonify({
                    "message": "Empresa atualizada com sucesso",
                    "company": result.data[0]
                }), 200
            else:
                return jsonify({"error": "Erro ao atualizar empresa"}), 500
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Buscar formas de pagamento da empresa
@company_bp.route('/api/company/<company_id>/payments')
def get_company_payments(company_id):
    try:
        if supabase:
            result = supabase.table('payment_companies').select('*').eq('id_company', company_id).execute()
            payments = result.data or []
            return jsonify({"payments": payments})
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Adicionar forma de pagamento
@company_bp.route('/api/company/<company_id>/payments', methods=['POST'])
def add_company_payment(company_id):
    try:
        data = request.get_json()
        
        required_fields = ['name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400

        payment_data = {
            'name': data.get('name'),
            'id_company': company_id
        }

        if supabase:
            result = supabase.table('payment_companies').insert(payment_data).execute()
            if result.data:
                return jsonify({
                    "message": "Forma de pagamento adicionada com sucesso",
                    "payment": result.data[0]
                }), 201
            else:
                return jsonify({"error": "Erro ao adicionar forma de pagamento"}), 500
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Deletar forma de pagamento
@company_bp.route('/api/company/<company_id>/payments/<payment_id>', methods=['DELETE'])
def delete_company_payment(company_id, payment_id):
    try:
        if supabase:
            result = supabase.table('payment_companies').delete().eq('id', payment_id).eq('id_company', company_id).execute()
            return jsonify({"message": "Forma de pagamento excluída com sucesso"}), 200
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500







