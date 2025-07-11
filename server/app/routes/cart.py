from flask import Blueprint, request, jsonify
from app.db import db, cursor

cart_bp = Blueprint("cart", __name__)

@cart_bp.route('/', methods=['GET'])
def get_cart():
    cursor.execute("""
      SELECT
        ci.id           AS cart_item_id,
        p.id            AS product_id,
        p.name,
        p.description,
        p.price,
        p.image_url,
        ci.quantity
      FROM cart_items ci
      JOIN products     p  ON p.id = ci.product_id
    """)
    items = cursor.fetchall()
    return jsonify(items), 200


@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data       = request.get_json()
    product_id = data['id']           # the product’s ID
    quantity   = data.get('quantity', 1)

    cursor.execute(
      "SELECT quantity FROM cart_items WHERE product_id = %s",
      (product_id,)
    )
    existing = cursor.fetchone()

    if existing:
        cursor.execute(
          "UPDATE cart_items SET quantity = quantity + %s WHERE product_id = %s",
          (quantity, product_id)
        )
    else:
        cursor.execute(
          "INSERT INTO cart_items (product_id, quantity) VALUES (%s, %s)",
          (product_id, quantity)
        )

    db.commit()
    return jsonify({"message": "Item added to cart"}), 201



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
    cursor.execute(
      "UPDATE cart_items SET quantity = greatest(quantity - 1, 0) WHERE id = %s",
      (item_id,)
    )
    db.commit()
    return jsonify({"message": "Quantity decreased"}), 200


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

