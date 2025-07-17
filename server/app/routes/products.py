from flask import Blueprint, request, jsonify
from app.db import get_db_connection

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_all_products():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(products), 200

@products_bp.route('/', methods=['POST'])
def add_product():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    data = request.get_json()
    name = data['name']
    price = data['price']
    image_url = data.get('image_url', '')
    description = data.get('description', '')

    cursor.execute(
        "INSERT INTO products (name, description, price, image_url) VALUES (%s, %s, %s, %s)",
        (name, price, image_url, description)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Product added"}), 201

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    db.close()
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404
