from flask import Blueprint, render_template, request, jsonify, session
from database import supabase
from datetime import datetime
import uuid

orders_bp = Blueprint('orders_bp', __name__)

# Página - Lista de pedidos ativos
@orders_bp.route('/orders/active')
def active_orders():
    return render_template('orders/active.html')

# Página - Pedidos de delivery
@orders_bp.route('/orders/delivery')
def delivery_orders():
    return render_template('orders/delivery.html')

# Página - Pedidos de mesa
@orders_bp.route('/orders/table')
def table_orders():
    return render_template('orders/table.html')

# Página - Histórico de pedidos
@orders_bp.route('/orders/history')
def orders_history():
    return render_template('orders/history.html')

# Página - Detalhes do pedido
@orders_bp.route('/orders/<order_id>')
def order_details(order_id):
    return render_template('orders/details.html', order_id=order_id)

# API - Buscar pedidos ativos
@orders_bp.route('/api/orders/active')
def get_active_orders():
    try:
        company_id = request.args.get('company_id', 'test-company-id')
        
        if supabase:
            # Buscar pedidos ativos (não finalizados)
            orders_result = supabase.table('orders').select('*').eq('id_company', company_id).neq('status', 'entregue').execute()
            orders = orders_result.data or []
            
            # Enriquecer com dados relacionados
            enriched_orders = []
            for order in orders:
                # Buscar dados do delivery se for delivery
                delivery_data = None
                if order.get('is_delivery'):
                    delivery_result = supabase.table('delivery').select('*').eq('id', order['id_order_delivery']).execute()
                    if delivery_result.data:
                        delivery_data = delivery_result.data[0]
                        
                        # Buscar dados do cliente
                        client_result = supabase.table('client').select('*').eq('id', delivery_data['id_client']).execute()
                        if client_result.data:
                            delivery_data['client'] = client_result.data[0]
                
                # Buscar produtos do pedido
                order_products_result = supabase.table('order_product').select('*').eq('id_order', order['id']).execute()
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
                
                enriched_order = {
                    **order,
                    'delivery': delivery_data,
                    'items': items,
                    'status': delivery_data['status'] if delivery_data else 'recebido'
                }
                enriched_orders.append(enriched_order)
            
            return jsonify({"orders": enriched_orders})
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Buscar pedidos de delivery
@orders_bp.route('/api/orders/delivery')
def get_delivery_orders():
    try:
        company_id = request.args.get('company_id', 'test-company-id')
        
        if supabase:
            # Buscar pedidos de delivery ativos
            orders_result = supabase.table('orders').select('*').eq('id_company', company_id).eq('is_delivery', True).neq('status', 'entregue').execute()
            orders = orders_result.data or []
            
            # Enriquecer com dados relacionados
            enriched_orders = []
            for order in orders:
                # Buscar dados do delivery
                delivery_result = supabase.table('delivery').select('*').eq('id', order['id_order_delivery']).execute()
                delivery_data = delivery_result.data[0] if delivery_result.data else None
                
                if delivery_data:
                    # Buscar dados do cliente
                    client_result = supabase.table('client').select('*').eq('id', delivery_data['id_client']).execute()
                    if client_result.data:
                        delivery_data['client'] = client_result.data[0]
                
                # Buscar produtos do pedido
                order_products_result = supabase.table('order_product').select('*').eq('id_order', order['id']).execute()
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
                
                enriched_order = {
                    **order,
                    'delivery': delivery_data,
                    'items': items,
                    'status': delivery_data['status'] if delivery_data else 'recebido'
                }
                enriched_orders.append(enriched_order)
            
            return jsonify({"orders": enriched_orders})
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Atualizar status do pedido
@orders_bp.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({"error": "Status é obrigatório"}), 400
        
        if supabase:
            # Buscar o pedido
            order_result = supabase.table('orders').select('*').eq('id', order_id).execute()
            if not order_result.data:
                return jsonify({"error": "Pedido não encontrado"}), 404
            
            order = order_result.data[0]
            
            # Se for delivery, atualizar status na tabela delivery
            if order.get('is_delivery') and order.get('id_order_delivery'):
                supabase.table('delivery').update({'status': new_status}).eq('id', order['id_order_delivery']).execute()
            
            # Se for mesa, atualizar status na tabela orders
            if order.get('is_table'):
                supabase.table('orders').update({'status': new_status}).eq('id', order_id).execute()
            
            return jsonify({"message": "Status atualizado com sucesso"}), 200
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Finalizar pedido
@orders_bp.route('/api/orders/<order_id>/finish', methods=['PUT'])
def finish_order(order_id):
    try:
        if supabase:
            # Buscar o pedido
            order_result = supabase.table('orders').select('*').eq('id', order_id).execute()
            if not order_result.data:
                return jsonify({"error": "Pedido não encontrado"}), 404
            
            order = order_result.data[0]
            
            # Criar registro em orders_finished
            finished_order = {
                'id_company': order['id_company'],
                'id_order': order['id'],
                'value': order['value']
            }
            supabase.table('orders_finished').insert(finished_order).execute()
            
            # Se for delivery, atualizar status para "entregue"
            if order.get('is_delivery') and order.get('id_order_delivery'):
                supabase.table('delivery').update({'status': 'entregue'}).eq('id', order['id_order_delivery']).execute()
            
            # Atualizar status do pedido para "entregue" em vez de deletar
            supabase.table('orders').update({'status': 'entregue'}).eq('id', order_id).execute()
            
            return jsonify({"message": "Pedido finalizado com sucesso"}), 200
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500
            
    except Exception as e:
        print(f"Erro ao finalizar pedido: {e}")
        return jsonify({"error": f"Erro ao finalizar pedido: {str(e)}"}), 500

# API - Buscar histórico de pedidos
@orders_bp.route('/api/orders/history')
def get_orders_history():
    try:
        company_id = request.args.get('company_id', 'test-company-id')
        
        if supabase:
            # Buscar pedidos finalizados
            orders_result = supabase.table('orders').select('*').eq('id_company', company_id).eq('status', 'entregue').execute()
            orders = orders_result.data or []
            
            # Enriquecer com dados relacionados
            enriched_orders = []
            for order in orders:
                # Buscar dados do delivery se for delivery
                delivery_data = None
                if order.get('is_delivery'):
                    delivery_result = supabase.table('delivery').select('*').eq('id', order['id_order_delivery']).execute()
                    if delivery_result.data:
                        delivery_data = delivery_result.data[0]
                        
                        # Buscar dados do cliente
                        client_result = supabase.table('client').select('*').eq('id', delivery_data['id_client']).execute()
                        if client_result.data:
                            delivery_data['client'] = client_result.data[0]
                
                # Buscar produtos do pedido
                order_products_result = supabase.table('order_product').select('*').eq('id_order', order['id']).execute()
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
                
                enriched_order = {
                    **order,
                    'delivery': delivery_data,
                    'items': items,
                    'status': delivery_data['status'] if delivery_data else 'entregue'
                }
                enriched_orders.append(enriched_order)
            
            return jsonify({"orders": enriched_orders})
        else:
            return jsonify({"error": "Banco de dados não configurado"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
