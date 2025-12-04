from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from typing import Any, Dict, List, cast

cart_bp = Blueprint("cart", __name__)

@cart_bp.route('/', methods=['GET'])
def get_cart():
  verify_jwt_in_request(optional=True)
  user_id = get_jwt_identity()

  db = get_db_connection()
  cursor = db.cursor()
  if user_id is None:
      cursor.execute("""
        SELECT ci.id AS cart_item_id, p.id AS product_id, p.name, p.description, p.price, p.image_url, ci.quantity
        FROM cart_items ci JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id IS NULL
      """)
  else:
      cursor.execute("""
        SELECT ci.id AS cart_item_id, p.id AS product_id, p.name, p.description, p.price, p.image_url, ci.quantity
        FROM cart_items ci JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id = %s
      """, (user_id,))
  items = cursor.fetchall()
  cursor.close(); db.close()
  return jsonify(items), 200


@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    verify_jwt_in_request(optional=True)
    user_id = get_jwt_identity()

    data       = request.get_json()
    product_id = data['id']           # the product’s ID
    quantity   = data.get('quantity', 1)

    db = get_db_connection()
    cursor = db.cursor()

    if user_id is None:
        cursor.execute(
          "SELECT quantity FROM cart_items WHERE product_id = %s AND user_id IS NULL",
          (product_id,)
        )
    else:
        cursor.execute(
          "SELECT quantity FROM cart_items WHERE product_id = %s AND user_id = %s",
          (product_id, user_id)
        )
    existing = cursor.fetchone()

    if existing:
        if user_id is None:
            cursor.execute(
              "UPDATE cart_items SET quantity = quantity + %s WHERE product_id = %s AND user_id IS NULL",
              (quantity, product_id)
            )
        else:
            cursor.execute(
              "UPDATE cart_items SET quantity = quantity + %s WHERE product_id = %s AND user_id = %s",
              (quantity, product_id, user_id)
            )
    else:
        cursor.execute(
          "INSERT INTO cart_items (product_id, quantity, user_id) VALUES (%s, %s, %s)",
          (product_id, quantity, user_id)
        )

    db.commit(); cursor.close(); db.close()
    return jsonify({"message": "Item added to cart"}), 201



@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Item removed"}), 200


@cart_bp.route('/increase/<int:item_id>', methods=['PATCH'])
def increase_quantity(item_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE cart_items SET quantity = quantity + 1 WHERE id = %s", (item_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Quantity increased"}), 200


@cart_bp.route('/decrease/<int:item_id>', methods=['PATCH'])
def decrease_quantity(item_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
      "UPDATE cart_items SET quantity = greatest(quantity - 1, 0) WHERE id = %s",
      (item_id,)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Quantity decreased"}), 200

@cart_bp.route("/checkout", methods=["POST"])
def checkout():
    # Try to pick up a token if one is present; don't error if it's missing
    verify_jwt_in_request(optional=True)
    user_id = get_jwt_identity()  # None if no (or invalid) token

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT ci.*, p.price
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
    """)
    # Cast to a list of dicts for static type checking
    items = cast(List[Dict[str, Any]], cur.fetchall())

    if not items:
        cur.close(); db.close()
        return jsonify(message="Cart is empty"), 400

    # Insert each cart_item into orders; if user_id is None, you
    # can insert a NULL or 0 in the user_id column (or skip that field entirely)
    for item in items:
        cur.execute(
            """
            INSERT INTO orders (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
            """,
            (user_id, int(item["product_id"]), int(item["quantity"]))
        )

    # clear the cart
    cur.execute("DELETE FROM cart_items")
    # If logged in, add points: $1 = 10 pts
    if user_id:
        # Calculate total spent in this checkout
        total_spent = sum(float(item["price"]) * int(item["quantity"]) for item in items)
        points_to_add = int(total_spent * 10)
        cur.execute(
            "UPDATE users SET points = points + %s WHERE id = %s",
            (points_to_add, user_id)
        )

    db.commit()
    cur.close(); db.close()

    if user_id:
        msg = "Thanks for checking out! Our loyal customers get 10% off their next order."
    else:
        msg = "Thanks for checking out! Please login to get 10% off your next order."

    return jsonify(message=msg), 200


