from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from app.__init__ import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from mysql.connector.errors import IntegrityError, Error as MySQLError
from typing import Any, Dict, cast

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    data = request.get_json()
    email    = data.get("email")
    username = data.get("username") or email  # allow email to serve as username
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg":"Missing credentials"}), 400

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    try:
        cursor.execute(
          "INSERT INTO users (email, username, password_hash) VALUES (%s,%s,%s)",
          (email, username, pw_hash)
        )
        db.commit()
    except IntegrityError as e:
        # 1062 = duplicate entry error code in MySQL
        if getattr(e, 'errno', None) == 1062:
            cursor.close(); db.close()
            return jsonify({"msg": "Username taken"}), 409
        else:
            cursor.close(); db.close()
            return jsonify({"msg": "Database integrity error", "detail": str(e)}), 400
    except MySQLError as e:
        cursor.close(); db.close()
        return jsonify({"msg": "Database error", "detail": str(e)}), 500

    cursor.close()
    db.close()
    return jsonify({"msg":"User created"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    data = request.get_json()
    identifier = data.get("identifier")   # could be 'boss' or 'boss@mail.com'
    password   = data.get("password")

    cursor.execute(
      """
      SELECT id, username, password_hash
      FROM users
      WHERE username = %s OR email = %s
      """,
      (identifier, identifier)
    )
    # MySQL connector returns dict rows when dictionary=True, but type stubs do not reflect this.
    # Cast to the expected dict type so static type checkers (e.g., Pyright) understand indexing by str.
    user_row = cursor.fetchone()
    user = cast(Dict[str, Any] | None, user_row)

    # If the user doesn't exist, abort early before attempting to access row fields.
    if user is None:
        cursor.close()
        db.close()
        return jsonify({"msg": "Bad credentials"}), 401

    # Validate password hash.
    if not bcrypt.check_password_hash(user["password_hash"], password):
        cursor.close()
        db.close()
        return jsonify({"msg": "Bad credentials"}), 401

    token = create_access_token(
              identity=str(user["id"]),
              additional_claims={"username": user["username"]}
            )

    # Attach any guest cart items (user_id IS NULL) to this user
    cursor.execute("UPDATE cart_items SET user_id = %s WHERE user_id IS NULL", (user["id"],))
    db.commit()
    # return in both body and header for convenience
    resp = jsonify({"access_token": token})
    resp.headers["Authorization"] = f"Bearer {token}"
    cursor.close()
    db.close()
    return resp, 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    user_id = int(get_jwt_identity())
    cursor.execute(
        "SELECT id, username, points FROM users WHERE id=%s", (user_id,)
    )
    u = cursor.fetchone()
    cursor.close()
    db.close()
    return jsonify(u), 200

