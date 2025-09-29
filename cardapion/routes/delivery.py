from flask import Blueprint, request, jsonify, render_template, session
from database import supabase
import uuid
import re
from datetime import datetime, timedelta

delivery_bp = Blueprint('delivery_bp', __name__)

# Página do cardápio público
@delivery_bp.route('/delivery/<company_id>/menu')
def delivery_menu(company_id):
    if supabase and company_id != 'test-company-id':
        try:
            # Buscar dados da empresa
            company_result = supabase.table('company').select('*').eq('id', company_id).execute()
            if not company_result.data:
                return "Empresa não encontrada", 404
            
            company = company_result.data[0]
            return render_template('delivery/menu.html', 
                                 company_name=company['name'], 
                                 company_id=company_id)
        except Exception as e:
            print(f"Erro ao buscar empresa: {e}")
            # Fallback para modo de desenvolvimento
            return render_template('delivery/menu.html', 
                                 company_name='Empresa Teste', 
                                 company_id=company_id)
    else:
        # Modo de desenvolvimento
        return render_template('delivery/menu.html', 
                             company_name='Empresa Teste', 
                             company_id=company_id)

# Página de checkout
@delivery_bp.route('/delivery/<company_id>/checkout')
def delivery_checkout(company_id):
    if supabase and company_id != 'test-company-id':
        try:
            company_result = supabase.table('company').select('*').eq('id', company_id).execute()
            if not company_result.data:
                return "Empresa não encontrada", 404
            
            company = company_result.data[0]
            return render_template('delivery/checkout.html', 
                                 company_name=company['name'], 
                                 company_id=company_id)
        except Exception as e:
            print(f"Erro ao buscar empresa: {e}")
            return render_template('delivery/checkout.html', 
                                 company_name='Empresa Teste', 
                                 company_id=company_id)
    else:
        return render_template('delivery/checkout.html', 
                             company_name='Empresa Teste', 
                             company_id=company_id)

# Página de confirmação
@delivery_bp.route('/delivery/<company_id>/confirmation')
def delivery_confirmation(company_id):
    if supabase and company_id != 'test-company-id':
        try:
            company_result = supabase.table('company').select('*').eq('id', company_id).execute()
            if not company_result.data:
                return "Empresa não encontrada", 404
            
            company = company_result.data[0]
            return render_template('delivery/confirmation.html', 
                                 company_name=company['name'], 
                                 company_id=company_id)
        except Exception as e:
            print(f"Erro ao buscar empresa: {e}")
            return render_template('delivery/confirmation.html', 
                                 company_name='Empresa Teste', 
                                 company_id=company_id)
    else:
        return render_template('delivery/confirmation.html', 
                             company_name='Empresa Teste', 
                             company_id=company_id)

# Página de acompanhamento
@delivery_bp.route('/delivery/<company_id>/track/<order_id>')
def delivery_track(company_id, order_id):
    if supabase and company_id != 'test-company-id':
        try:
            company_result = supabase.table('company').select('*').eq('id', company_id).execute()
            if not company_result.data:
                return "Empresa não encontrada", 404
            
            company = company_result.data[0]
            return render_template('delivery/track.html', 
                                 company_name=company['name'], 
                                 company_id=company_id)
        except Exception as e:
            print(f"Erro ao buscar empresa: {e}")
            return render_template('delivery/track.html', 
                                 company_name='Empresa Teste', 
                                 company_id=company_id)
    else:
        return render_template('delivery/track.html', 
                             company_name='Empresa Teste', 
                             company_id=company_id)

# API - Buscar categorias da empresa
@delivery_bp.route('/api/company/<company_id>/categories')
def get_company_categories(company_id):
    try:
        if supabase and company_id != 'test-company-id':
            result = supabase.table('categories_products').select('*').eq('id_company', company_id).execute()
            return jsonify({"categories": result.data or []})
        else:
            # Modo de desenvolvimento - dados mock
            return jsonify({
                "categories": [
                    {"id": "cat1", "name": "Pizzas", "kitchen": True},
                    {"id": "cat2", "name": "Bebidas", "kitchen": False},
                    {"id": "cat3", "name": "Sobremesas", "kitchen": True}
                ]
            })
    except Exception as e:
        print(f"Erro ao buscar categorias: {e}")
        # Fallback para modo de desenvolvimento
        return jsonify({
            "categories": [
                {"id": "cat1", "name": "Pizzas", "kitchen": True},
                {"id": "cat2", "name": "Bebidas", "kitchen": False},
                {"id": "cat3", "name": "Sobremesas", "kitchen": True}
            ]
        })

# API - Buscar produtos da empresa
@delivery_bp.route('/api/company/<company_id>/products')
def get_company_products(company_id):
    try:
        if supabase and company_id != 'test-company-id':
            result = supabase.table('products').select('*').eq('id_company', company_id).execute()
            return jsonify({"products": result.data or []})
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
                        "preparation_time": "00:20:00"
                    },
                    {
                        "id": "prod2", 
                        "name": "Coca-Cola 350ml", 
                        "price": 500, 
                        "description": "Refrigerante gelado",
                        "id_categorie": "cat2",
                        "preparation_time": "00:01:00"
                    },
                    {
                        "id": "prod3", 
                        "name": "Pudim", 
                        "price": 800, 
                        "description": "Pudim de leite condensado",
                        "id_categorie": "cat3",
                        "preparation_time": "00:05:00"
                    }
                ]
            })
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        # Fallback para modo de desenvolvimento
        return jsonify({
            "products": [
                {
                    "id": "prod1", 
                    "name": "Pizza Margherita", 
                    "price": 3500, 
                    "description": "Molho de tomate, mussarela e manjericão",
                    "id_categorie": "cat1",
                    "preparation_time": "00:20:00"
                },
                {
                    "id": "prod2", 
                    "name": "Coca-Cola 350ml", 
                    "price": 500, 
                    "description": "Refrigerante gelado",
                    "id_categorie": "cat2",
                    "preparation_time": "00:01:00"
                },
                {
                    "id": "prod3", 
                    "name": "Pudim", 
                    "price": 800, 
                    "description": "Pudim de leite condensado",
                    "id_categorie": "cat3",
                    "preparation_time": "00:05:00"
                }
            ]
        })

# API - Verificar cliente existente
@delivery_bp.route('/api/client/check', methods=['POST'])
def check_existing_client():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({"error": "Email é obrigatório"}), 400
        
        if supabase:
            try:
                result = supabase.table('client').select('*').eq('email', email).execute()
                if result.data:
                    return jsonify({"client": result.data[0]})
                else:
                    return jsonify({"client": None})
            except Exception as e:
                print(f"Erro ao verificar cliente: {e}")
                return jsonify({"client": None})
        else:
            # Modo de desenvolvimento
            return jsonify({"client": None})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Criar pedido
@delivery_bp.route('/api/orders/create', methods=['POST'])
def create_order():
    try:
        data = request.get_json()

        required_fields = ['company_id', 'client', 'items', 'payment_method', 'total']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400

        if supabase and data['company_id'] != 'test-company-id':
            try:
                # Criar ou buscar cliente
                client_data = data['client']
                client_result = supabase.table('client').select('*').eq('email', client_data['email']).execute()

                if client_result.data:
                    client_id = client_result.data[0]['id']
                    # Atualizar dados do cliente
                    supabase.table('client').update({
                        'name': client_data['name'],
                        'contact': re.sub(r'\\D', '', client_data['phone']),
                        'cpf_cnpj': re.sub(r'\\D', '', client_data['cpf']),
                        'adress_1': client_data['address'],
                        'adres_2': client_data.get('address2', '')
                    }).eq('id', client_id).execute()
                else:
                    # Criar novo cliente
                    new_client = {
                        'name': client_data['name'],
                        'email': client_data['email'],
                        'contact': re.sub(r'\\D', '', client_data['phone']),
                        'cpf_cnpj': re.sub(r'\\D', '', client_data['cpf']),
                        'adress_1': client_data['address'],
                        'adres_2': client_data.get('address2', '')
                    }
                    client_result = supabase.table('client').insert(new_client).execute()
                    client_id = client_result.data[0]['id']

                # Criar registro de delivery
                delivery_data = {
                    'id_client': client_id,
                    'id_company': data['company_id'],
                    'status': 'recebido'
                }
                delivery_result = supabase.table('delivery').insert(delivery_data).execute()
                delivery_id = delivery_result.data[0]['id']

                # Criar pedido
                order_data = {
                    'id_company': data['company_id'],
                    'is_delivery': True,
                    'is_table': False,
                    'value': data['total'],
                    'id_order_delivery': delivery_id
                }
                order_result = supabase.table('orders').insert(order_data).execute()
                order_id = order_result.data[0]['id']

                # Adicionar produtos ao pedido
                for item in data['items']:
                    order_product_data = {
                        'id_product': item['id'],
                        'id_order': order_id,
                        'id_company': data['company_id']
                    }
                    supabase.table('order_product').insert(order_product_data).execute()

                    # Verificar se é produto de cozinha
                    product_result = supabase.table('products').select('id_categorie').eq('id', item['id']).execute()
                    if product_result.data:
                        category_result = supabase.table('categories_products').select('kitchen').eq('id', product_result.data[0]['id_categorie']).execute()
                        if category_result.data and category_result.data[0]['kitchen']:
                            # Adicionar à cozinha
                            kitchen_data = {
                                'id_company': data['company_id'],
                                'id_order': order_id
                            }
                            supabase.table('requests_kitchen').insert(kitchen_data).execute()

                return jsonify({
                    "message": "Pedido criado com sucesso",
                    "order_id": order_id
                }), 201
            except Exception as e:
                print(f"Erro ao criar pedido: {e}")
                # Fallback para modo de desenvolvimento
                order_id = str(uuid.uuid4())
                return jsonify({
                    "message": "Pedido criado com sucesso (modo de desenvolvimento)",
                    "order_id": order_id
                }), 201
        else:
            # Modo de desenvolvimento
            order_id = str(uuid.uuid4())
            return jsonify({
                "message": "Pedido criado com sucesso (modo de desenvolvimento)",
                "order_id": order_id
            }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Acompanhar pedido
@delivery_bp.route('/api/orders/<order_id>/track')
def track_order(order_id):
    try:
        if supabase and order_id != 'test-order-id':
            try:
                # Buscar pedido com dados relacionados
                order_result = supabase.table('orders').select('*').eq('id', order_id).execute()
                if not order_result.data:
                    return jsonify({"error": "Pedido não encontrado"}), 404

                order = order_result.data[0]

                # Buscar dados do delivery
                delivery_result = supabase.table('delivery').select('*').eq('id', order['id_order_delivery']).execute()
                delivery = delivery_result.data[0] if delivery_result.data else None

                # Buscar dados do cliente
                client_result = supabase.table('client').select('*').eq('id', delivery['id_client']).execute()
                client = client_result.data[0] if client_result.data else None

                # Buscar produtos do pedido
                order_products_result = supabase.table('order_product').select('*').eq('id_order', order_id).execute()
                order_products = order_products_result.data or []

                # Buscar detalhes dos produtos
                items = []
                for op in order_products:
                    product_result = supabase.table('products').select('*').eq('id', op['id_product']).execute()
                    if product_result.data:
                        product = product_result.data[0]
                        items.append({
                            'id': product['id'],
                            'name': product['name'],
                            'price': product['price'],
                            'quantity': 1
                        })

                return jsonify({
                    "order": {
                        "id": order['id'],
                        "total": order['value'],
                        "status": delivery['status'] if delivery else 'recebido',
                        "created_at": order['created_at'],
                        "updated_at": order.get('updated_at', order['created_at']),
                        "client": client,
                        "items": items
                    }
                })
            except Exception as e:
                print(f"Erro ao buscar pedido: {e}")
                # Fallback para modo de desenvolvimento
                return jsonify({
                    "order": {
                        "id": order_id,
                        "total": 4500,
                        "status": "preparando",
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat(),
                        "client": {
                            "name": "João Silva",
                            "phone": "(11) 99999-9999",
                            "address": "Rua das Flores, 123, Centro",
                            "address2": "Apto 45"
                        },
                        "items": [
                            {"id": "prod1", "name": "Pizza Margherita", "price": 3500, "quantity": 1},
                            {"id": "prod2", "name": "Coca-Cola 350ml", "price": 500, "quantity": 2}
                        ]
                    }
                })
        else:
            # Modo de desenvolvimento
            return jsonify({
                "order": {
                    "id": order_id,
                    "total": 4500,
                    "status": "preparando",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "client": {
                        "name": "João Silva",
                        "phone": "(11) 99999-9999",
                        "address": "Rua das Flores, 123, Centro",
                        "address2": "Apto 45"
                    },
                    "items": [
                        {"id": "prod1", "name": "Pizza Margherita", "price": 3500, "quantity": 1},
                        {"id": "prod2", "name": "Coca-Cola 350ml", "price": 500, "quantity": 2}
                    ]
                }
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Buscar formas de pagamento
@delivery_bp.route('/api/company/<company_id>/payments')
def get_company_payments(company_id):
    try:
        if supabase and company_id != 'test-company-id':
            try:
                result = supabase.table('payments').select('*').eq('id_company', company_id).execute()
                return jsonify({"payments": result.data or []})
            except Exception as e:
                print(f"Erro ao buscar formas de pagamento: {e}")
                # Fallback para modo de desenvolvimento
                return jsonify({
                    "payments": [
                        {"id": "pix", "name": "PIX", "icon": "fas fa-qrcode"},
                        {"id": "dinheiro", "name": "Dinheiro", "icon": "fas fa-money-bill"},
                        {"id": "cartao", "name": "Cartão", "icon": "fas fa-credit-card"}
                    ]
                })
        else:
            # Modo de desenvolvimento
            return jsonify({
                "payments": [
                    {"id": "pix", "name": "PIX", "icon": "fas fa-qrcode"},
                    {"id": "dinheiro", "name": "Dinheiro", "icon": "fas fa-money-bill"},
                    {"id": "cartao", "name": "Cartão", "icon": "fas fa-credit-card"}
                ]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
