from flask import Blueprint, request, jsonify
from db import db, cursor

cart_bp = Blueprint("cart", __name__)

@cart_bp.route('/', methods=['GET'])
def get_cart():
    cursor.execute("SELECT * FROM cart_items")
    return jsonify(cursor.fetchall())

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    # logic to add item to cart
    data = request.get_json()
    name = data['name']
    price = data['price']
    image_url = data.get('image_url', '')
    description = data.get('description', '')
    cursor.execute(
        "INSERT INTO cart (name, description, price, image_url) VALUES (%s, %s, %s, %s)",
        (name, description, price, image_url)
    )
    db.commit()
    return jsonify({"message": "Item added to Cart"}), 201



