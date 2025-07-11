from flask import Blueprint, jsonify
from app.db import cursor

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
def get_orders():
    cursor.execute("""
      SELECT
        o.id           AS order_item_id,
        o.created_at   AS created_at,
        o.product_id   AS product_id,
        p.name         AS name,
        p.description  AS description,
        p.price        AS price,
        p.image_url    AS image_url,
        o.quantity     AS quantity
      FROM orders o
      JOIN products p ON p.id = o.product_id
      ORDER BY o.created_at DESC
    """)
    orders = cursor.fetchall()
    return jsonify(orders), 200

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    cursor.execute("""
      SELECT
        o.id           AS order_item_id,
        o.created_at   AS created_at,
        o.product_id,
        p.name,
        p.description,
        p.price,
        p.image_url,
        o.quantity
      FROM orders o
      JOIN products p ON p.id = o.product_id
      WHERE o.id = %s
    """, (order_id,))
    order = cursor.fetchone()
    if order:
        return jsonify(order), 200
    return jsonify({'message': 'Order not found'}), 404
