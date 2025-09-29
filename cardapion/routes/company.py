import re
from flask import Blueprint, request,jsonify
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







