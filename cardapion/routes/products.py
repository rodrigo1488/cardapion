from flask import Blueprint, request, jsonify, render_template, session
from database import supabase
import uuid
from routes.auth import login_required

products_bp = Blueprint('products_bp', __name__)

# Página de listagem de produtos
@products_bp.route('/products')
@login_required
def products_list():
    return render_template('products/list.html')

# Página de criação de produto
@products_bp.route('/products/new')
@login_required
def products_new():
    return render_template('products/form.html')

# Página de edição de produto
@products_bp.route('/products/<product_id>/edit')
@login_required
def products_edit(product_id):
    return render_template('products/form.html', product_id=product_id)

# API - Listar produtos da empresa
@products_bp.route('/api/products')
@login_required
def get_products():
    try:
        company_id = session.get('company_id')
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('products').select('*, categories_products(name)').eq('id_company', company_id).order('created_at', desc=True).execute()
                return jsonify({"products": result.data or []})
            except Exception as e:
                print(f"Erro ao buscar produtos: {e}")
                return jsonify({"products": []})
        else:
            # Modo de desenvolvimento - dados mock
            return jsonify({
                "products": [
                    {
                        "id": "prod1",
                        "name": "Pizza Margherita",
                        "price": 3500,
                        "description": "Molho de tomate, mussarela e manjericão",
                        "id_categorie": "cat1",
                        "preparation_time": "00:20:00",
                        "categories_products": {"name": "Pizzas"},
                        "created_at": "2024-01-01T10:00:00Z"
                    },
                    {
                        "id": "prod2",
                        "name": "Coca-Cola 350ml",
                        "price": 500,
                        "description": "Refrigerante gelado",
                        "id_categorie": "cat2",
                        "preparation_time": "00:01:00",
                        "categories_products": {"name": "Bebidas"},
                        "created_at": "2024-01-01T10:00:00Z"
                    },
                    {
                        "id": "prod3",
                        "name": "Pudim",
                        "price": 800,
                        "description": "Pudim de leite condensado",
                        "id_categorie": "cat3",
                        "preparation_time": "00:05:00",
                        "categories_products": {"name": "Sobremesas"},
                        "created_at": "2024-01-01T10:00:00Z"
                    }
                ]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Buscar produto específico
@products_bp.route('/api/products/<product_id>')
@login_required
def get_product(product_id):
    try:
        company_id = session.get('company_id')
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('products').select('*, categories_products(name)').eq('id', product_id).eq('id_company', company_id).execute()
                if not result.data:
                    return jsonify({"error": "Produto não encontrado"}), 404
                return jsonify({"product": result.data[0]})
            except Exception as e:
                print(f"Erro ao buscar produto: {e}")
                return jsonify({"error": "Erro ao buscar produto"}), 500
        else:
            # Modo de desenvolvimento
            return jsonify({
                "product": {
                    "id": product_id,
                    "name": "Pizza Margherita",
                    "price": 3500,
                    "description": "Molho de tomate, mussarela e manjericão",
                    "id_categorie": "cat1",
                    "preparation_time": "00:20:00",
                    "categories_products": {"name": "Pizzas"}
                }
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Criar produto
@products_bp.route('/api/products', methods=['POST'])
@login_required
def create_product():
    try:
        data = request.get_json()
        company_id = session.get('company_id')
        
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        required_fields = ['name', 'price', 'id_categorie']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400

        # Converter preço para centavos
        price = int(float(data.get('price')) * 100)

        product_data = {
            'name': data.get('name'),
            'price': price,
            'description': data.get('description', ''),
            'id_categorie': data.get('id_categorie'),
            'preparation_time': data.get('preparation_time', '00:15:00'),
            'id_company': company_id
        }

        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('products').insert(product_data).execute()
                if result.data:
                    return jsonify({
                        "message": "Produto criado com sucesso",
                        "product": result.data[0]
                    }), 201
                else:
                    return jsonify({"error": "Erro ao criar produto"}), 500
            except Exception as e:
                print(f"Erro ao criar produto: {e}")
                return jsonify({"error": "Erro ao criar produto"}), 500
        else:
            # Modo de desenvolvimento
            product_id = str(uuid.uuid4())
            return jsonify({
                "message": "Produto criado com sucesso (modo de desenvolvimento)",
                "product": {
                    "id": product_id,
                    "name": product_data['name'],
                    "price": product_data['price'],
                    "description": product_data['description'],
                    "id_categorie": product_data['id_categorie'],
                    "preparation_time": product_data['preparation_time'],
                    "id_company": company_id
                }
            }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Atualizar produto
@products_bp.route('/api/products/<product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    try:
        data = request.get_json()
        company_id = session.get('company_id')
        
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        required_fields = ['name', 'price', 'id_categorie']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400

        # Converter preço para centavos
        price = int(float(data.get('price')) * 100)

        update_data = {
            'name': data.get('name'),
            'price': price,
            'description': data.get('description', ''),
            'id_categorie': data.get('id_categorie'),
            'preparation_time': data.get('preparation_time', '00:15:00')
        }

        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('products').update(update_data).eq('id', product_id).eq('id_company', company_id).execute()
                if result.data:
                    return jsonify({
                        "message": "Produto atualizado com sucesso",
                        "product": result.data[0]
                    }), 200
                else:
                    return jsonify({"error": "Produto não encontrado"}), 404
            except Exception as e:
                print(f"Erro ao atualizar produto: {e}")
                return jsonify({"error": "Erro ao atualizar produto"}), 500
        else:
            # Modo de desenvolvimento
            return jsonify({
                "message": "Produto atualizado com sucesso (modo de desenvolvimento)",
                "product": {
                    "id": product_id,
                    "name": update_data['name'],
                    "price": update_data['price'],
                    "description": update_data['description'],
                    "id_categorie": update_data['id_categorie'],
                    "preparation_time": update_data['preparation_time'],
                    "id_company": company_id
                }
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Deletar produto
@products_bp.route('/api/products/<product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    try:
        company_id = session.get('company_id')
        
        if not company_id:
            return jsonify({"error": "Empresa não encontrada na sessão"}), 400

        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('products').delete().eq('id', product_id).eq('id_company', company_id).execute()
                return jsonify({"message": "Produto excluído com sucesso"}), 200
            except Exception as e:
                print(f"Erro ao deletar produto: {e}")
                return jsonify({"error": "Erro ao excluir produto"}), 500
        else:
            # Modo de desenvolvimento
            return jsonify({"message": "Produto excluído com sucesso (modo de desenvolvimento)"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
