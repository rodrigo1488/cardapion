from flask import Blueprint, request, jsonify, render_template, session
from database import supabase
import uuid
from routes.auth import login_required

categories_bp = Blueprint('categories_bp', __name__)

# Página de listagem de categorias
@categories_bp.route('/categories')
@login_required
def categories_list():
    return render_template('categories/list.html')

# Página de criação de categoria
@categories_bp.route('/categories/new')
@login_required
def categories_new():
    return render_template('categories/form.html')

# Página de edição de categoria
@categories_bp.route('/categories/<category_id>/edit')
@login_required
def categories_edit(category_id):
    return render_template('categories/form.html', category_id=category_id)

# API - Listar categorias da empresa
@categories_bp.route('/api/categories')
@login_required
def get_categories():
    try:
        company_id = session.get('company_id')
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('categories_products').select('*').eq('id_company', company_id).order('created_at', desc=True).execute()
                return jsonify({"categories": result.data or []})
            except Exception as e:
                print(f"Erro ao buscar categorias: {e}")
                return jsonify({"categories": []})
        else:
            # Modo de desenvolvimento - dados mock
            return jsonify({
                "categories": [
                    {
                        "id": "cat1",
                        "name": "Pizzas",
                        "kitchen": True,
                        "created_at": "2024-01-01T10:00:00Z"
                    },
                    {
                        "id": "cat2", 
                        "name": "Bebidas",
                        "kitchen": False,
                        "created_at": "2024-01-01T10:00:00Z"
                    },
                    {
                        "id": "cat3",
                        "name": "Sobremesas", 
                        "kitchen": True,
                        "created_at": "2024-01-01T10:00:00Z"
                    }
                ]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Buscar categoria específica
@categories_bp.route('/api/categories/<category_id>')
@login_required
def get_category(category_id):
    try:
        company_id = session.get('company_id')
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('categories_products').select('*').eq('id', category_id).eq('id_company', company_id).execute()
                if not result.data:
                    return jsonify({"error": "Categoria não encontrada"}), 404
                return jsonify({"category": result.data[0]})
            except Exception as e:
                print(f"Erro ao buscar categoria: {e}")
                return jsonify({"error": "Erro ao buscar categoria"}), 500
        else:
            # Modo de desenvolvimento
            return jsonify({
                "category": {
                    "id": category_id,
                    "name": "Pizza",
                    "kitchen": True
                }
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Criar categoria
@categories_bp.route('/api/categories', methods=['POST'])
@login_required
def create_category():
    try:
        data = request.get_json()
        company_id = session.get('company_id')
        
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        required_fields = ['name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400

        category_data = {
            'name': data.get('name'),
            'kitchen': data.get('kitchen', True),
            'id_company': company_id
        }

        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('categories_products').insert(category_data).execute()
                if result.data:
                    return jsonify({
                        "message": "Categoria criada com sucesso",
                        "category": result.data[0]
                    }), 201
                else:
                    return jsonify({"error": "Erro ao criar categoria"}), 500
            except Exception as e:
                print(f"Erro ao criar categoria: {e}")
                return jsonify({"error": "Erro ao criar categoria"}), 500
        else:
            # Modo de desenvolvimento
            category_id = str(uuid.uuid4())
            return jsonify({
                "message": "Categoria criada com sucesso (modo de desenvolvimento)",
                "category": {
                    "id": category_id,
                    "name": category_data['name'],
                    "kitchen": category_data['kitchen'],
                    "id_company": company_id
                }
            }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Atualizar categoria
@categories_bp.route('/api/categories/<category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    try:
        data = request.get_json()
        company_id = session.get('company_id')
        
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        required_fields = ['name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400

        update_data = {
            'name': data.get('name'),
            'kitchen': data.get('kitchen', True)
        }

        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('categories_products').update(update_data).eq('id', category_id).eq('id_company', company_id).execute()
                if result.data:
                    return jsonify({
                        "message": "Categoria atualizada com sucesso",
                        "category": result.data[0]
                    }), 200
                else:
                    return jsonify({"error": "Categoria não encontrada"}), 404
            except Exception as e:
                print(f"Erro ao atualizar categoria: {e}")
                return jsonify({"error": "Erro ao atualizar categoria"}), 500
        else:
            # Modo de desenvolvimento
            return jsonify({
                "message": "Categoria atualizada com sucesso (modo de desenvolvimento)",
                "category": {
                    "id": category_id,
                    "name": update_data['name'],
                    "kitchen": update_data['kitchen'],
                    "id_company": company_id
                }
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Deletar categoria
@categories_bp.route('/api/categories/<category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    try:
        company_id = session.get('company_id')
        
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        if supabase and company_id != 'test-company-id':
            try:
                # Verificar se há produtos nesta categoria
                products_result = supabase.table('products').select('id').eq('id_categorie', category_id).eq('id_company', company_id).execute()
                if products_result.data:
                    return jsonify({"error": "Não é possível excluir categoria que possui produtos"}), 400

                result = supabase.table('categories_products').delete().eq('id', category_id).eq('id_company', company_id).execute()
                return jsonify({"message": "Categoria excluída com sucesso"}), 200
            except Exception as e:
                print(f"Erro ao deletar categoria: {e}")
                return jsonify({"error": "Erro ao excluir categoria"}), 500
        else:
            # Modo de desenvolvimento
            return jsonify({"message": "Categoria excluída com sucesso (modo de desenvolvimento)"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
