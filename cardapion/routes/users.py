from flask import Blueprint, request, jsonify
from database import supabase


users_bp = Blueprint('users_bp',"__name__")

@users_bp.route("/create_user", methods = ["POST"])
def create_user():
    try:
        data = request.get_json()
        required_fields = ['name', 'email','password','id_company']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"o campo {field} é obrigatorio!"})
        if supabase:
            existing_user_company = supabase.table('users_company').select('*').eq('email',data.get('email')).eq('id_company', data.get('id_company')).execute()

            if existing_user_company.data:
                return jsonify({"error": "o email já está em uso!"})
            
            user_data = {
                "name": data.get('name'),
                "email": data.get('email'),
                "password": data.get('password'),
                "id_company": data.get('id_company')
            }


        result = supabase.table('users_company').insert(user_data).execute()
        if result.data:
            return jsonify({"message": "usuario criado com sucesso!"}),201
        else:
            return jsonify({"error": "erro ao criar o usuario, tente novamente mais tarde"}),500
        
    except Exception as e:
        return jsonify({"error": str(e)}),500
            
