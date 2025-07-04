from flask import Blueprint, request, jsonify
from app.db import db, cursor

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
def get_orders():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return jsonify(orders)

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    if order:
        return jsonify(order)
    return jsonify({'message': 'Order not found'}), 404
