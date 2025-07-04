from flask import Blueprint, request, jsonify
from app.db import db, cursor

cart_bp = Blueprint("cart", __name__)


@cart_bp.route('/', methods=['GET'])
def get_cart():
    cursor.execute("SELECT * FROM cart_items")
    return jsonify(cursor.fetchall())


@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
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


@cart_bp.route('/cart', methods=['GET'])
def get_cart_items():
    cursor.execute("SELECT * FROM cart_items")
    cart_items = cursor.fetchall()
    return jsonify(cart_items)


@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    cursor.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
    db.commit()
    return jsonify({"message": "Item removed"}), 200


@cart_bp.route('/increase/<int:item_id>', methods=['PATCH'])
def increase_quantity(item_id):
    cursor.execute(
        "UPDATE cart_items SET quantity = quantity + 1 WHERE id = %s", (item_id,))
    db.commit()
    return jsonify({"message": "Quantity increased"}), 200


@cart_bp.route('/decrease/<int:item_id>', methods=['PATCH'])
def decrease_quantity(item_id):
    # Ensure quantity doesn't go below 1
    cursor.execute("SELECT quantity FROM cart_items WHERE id = %s", (item_id,))
    result = cursor.fetchone()
    if result and result[0] > 1:
        cursor.execute(
            "UPDATE cart_items SET quantity = quantity - 1 WHERE id = %s", (item_id,))
        db.commit()
        return jsonify({"message": "Quantity decreased"}), 200
    else:
        return jsonify({"message": "Cannot decrease quantity below 1"}), 400


@cart_bp.route('/checkout', methods=['POST'])
def checkout():
    cursor.execute("SELECT * FROM cart_items")
    items = cursor.fetchall()

    if not items:
        return jsonify({"message": "Cart is already empty!"}), 400

    for item in items:
        cursor.execute(
            "INSERT INTO orders (product_id, quantity) VALUES (%s, %s)",
            (item['product_id'], item['quantity'])
        )

    # Clear cart
    cursor.execute("DELETE FROM cart_items")
    db.commit()

    return jsonify({"message": "Checkout successful!"}), 200

