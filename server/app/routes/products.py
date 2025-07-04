from flask import Blueprint, request, jsonify
from app.db import db, cursor 

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_all_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products), 200

@products_bp.route('/', methods=['POST'])
def add_product():
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
    return jsonify({"message": "Product added"}), 201
