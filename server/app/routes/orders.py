from flask import Blueprint, jsonify
from app.db import get_db_connection
from collections import defaultdict
from datetime import datetime
from typing import cast, List, Dict, Any
from flask_jwt_extended import jwt_required, get_jwt_identity


orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    user_id = get_jwt_identity()
    cursor.execute("""
      SELECT
        o.id           AS order_item_id,
        o.created_at   AS created_at,
        o.status       AS status,
        o.product_id   AS product_id,
        p.name         AS name,
        p.description  AS description,
        p.price        AS price,
        p.image_url    AS image_url,
        o.quantity     AS quantity
      FROM orders o
      JOIN products p ON p.id = o.product_id
      WHERE o.user_id = %s
      ORDER BY o.created_at DESC
    """, (user_id,))
    rows = cast(List[Dict[str, Any]], cursor.fetchall())    
    cursor.close()
    db.close()

    grouped = defaultdict(list)
    for row in rows:
        created_val = row['created_at']
        if isinstance(created_val, str):
            created = created_val
        else:
            created = created_val.strftime('%Y-%m-%d %H:%M:%S')
        grouped[created].append(row)

    result = []
    for created, items in grouped.items():
        total = sum(float(item['price']) * int(item['quantity']) for item in items)
        status = items[0]['status']
        result.append({
            "order_id": created.replace(' ', '').replace(':', '').replace('-', ''),
            "created_at": created,
            "status": status,
            "items": [
                {
                  "id": item['product_id'],
                  "name": item['name'],
                  "image_url": item['image_url'],
                  "quantity": int(item['quantity']),
                  "price": float(item['price'])
                } for item in items
            ],
            "total": round(total, 2)
        })

    return jsonify(result), 200


@orders_bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    user_id = get_jwt_identity()
    cursor.execute("""
      SELECT
        o.id           AS order_item_id,
        o.created_at   AS created_at,
        o.status       AS status,
        o.product_id,
        p.name,
        p.description,
        p.price,
        p.image_url,
        o.quantity
      FROM orders o
      JOIN products p ON p.id = o.product_id
      WHERE DATE_FORMAT(o.created_at, '%%Y%%m%%d%%H%%i%%s') = %s
        AND o.user_id = %s
    """, (order_id, user_id))
    rows = cast(List[Dict[str, Any]], cursor.fetchall())    
    cursor.close()
    db.close()

    if not rows:
        return jsonify({'message': 'Order not found'}), 404

    total = sum(float(item['price']) * int(item['quantity']) for item in rows)

    created_at_value = rows[0]['created_at']
    if isinstance(created_at_value, str):
        created_at = created_at_value
    else:
        created_at = created_at_value.strftime('%Y-%m-%d %H:%M:%S')
    status = rows[0]['status']

    order = {
        "order_id": order_id,
        "created_at": created_at,
        "status": status,
        "items": [
            {
                "id": item['product_id'],
                "name": item['name'],
                "image_url": item['image_url'],
                "quantity": int(item['quantity']),
                "price": float(item['price'])
            } for item in rows
        ],
        "total": round(total, 2)
    }
    return jsonify(order), 200
