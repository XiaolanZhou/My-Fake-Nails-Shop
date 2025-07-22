from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_all_products():
    q          = request.args.get('q', '')
    page       = int(request.args.get('page', 1))
    per_page   = int(request.args.get('per_page', 8))
    price_min  = request.args.get('price_min')
    price_max  = request.args.get('price_max')
    sort = request.args.get('sort', '')  # 'price_asc', 'price_desc', 'rating'

    filters = []
    params  = []
    if q:
        filters.append("(name LIKE %s OR description LIKE %s)")
        wildcard = f"%{q}%"
        params.extend([wildcard, wildcard])
    if price_min is not None:
        filters.append("price >= %s")
        params.append(price_min)
    if price_max is not None:
        filters.append("price <= %s")
        params.append(price_max)

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""

    offset = (page - 1) * per_page

    order_clause = ""
    if sort == 'price_asc':
        order_clause = "ORDER BY price ASC"
    elif sort == 'price_desc':
        order_clause = "ORDER BY price DESC"
    elif sort == 'rating':
        order_clause = "ORDER BY rating DESC"  # assumes rating column or view

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get total count
    cursor.execute(f"SELECT COUNT(*) AS cnt FROM products {where_clause}", params)
    total_row = cursor.fetchone()  # type: ignore[assignment]
    total = int(total_row["cnt"] if total_row else 0)  # type: ignore[index]

    # Fetch page of data
    cursor.execute(
        f"SELECT * FROM products {where_clause} {order_clause} LIMIT %s OFFSET %s",
        params + [per_page, offset]
    )
    products = cursor.fetchall()
    cursor.close(); db.close()

    return jsonify({
        "items": products,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page,
    }), 200

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

@products_bp.route('/<int:product_id>/rate', methods=['POST'])
@jwt_required()
def rate_product(product_id):
    user_id = int(get_jwt_identity())
    rating = request.get_json().get('rating')
    if rating is None or not (1 <= int(rating) <= 5):
        return jsonify({'message': 'Rating must be 1-5'}), 400

    db = get_db_connection()
    cur = db.cursor()

    # Insert or update individual rating
    cur.execute(
        """
        INSERT INTO product_ratings (product_id, user_id, rating)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE rating = VALUES(rating)
        """,
        (product_id, user_id, rating)
    )

    # Recalculate aggregate
    cur.execute(
        """
        SELECT AVG(rating) AS avg_rating, COUNT(*) AS cnt
        FROM product_ratings
        WHERE product_id = %s
        """,
        (product_id,)
    )
    row = cur.fetchone()
    avg_rating = float(row[0] or 0) if row else 0.0  # type: ignore[index]
    cnt = int(row[1] or 0) if row else 0  # type: ignore[index]

    cur.execute(
        "UPDATE products SET rating=%s, rating_count=%s WHERE id=%s",
        (avg_rating, cnt, product_id)
    )

    db.commit(); cur.close(); db.close()
    return jsonify({'rating': avg_rating, 'count': cnt}), 200
