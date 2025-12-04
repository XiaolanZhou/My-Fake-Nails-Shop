from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from app import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from psycopg2 import IntegrityError, Error as DBError
from typing import Any, Dict, cast

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    db = get_db_connection()
    cursor = db.cursor()
    data = request.get_json()
    email    = data.get("email")
    username = data.get("username") or email
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
        db.rollback()
        cursor.close(); db.close()
        return jsonify({"msg": "Username or email already taken"}), 409
    except DBError as e:
        db.rollback()
        cursor.close(); db.close()
        return jsonify({"msg": "Database error", "detail": str(e)}), 500

    cursor.close()
    db.close()
    return jsonify({"msg":"User created"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    db = get_db_connection()
    cursor = db.cursor()
    data = request.get_json()
    identifier = data.get("identifier")
    password   = data.get("password")

    cursor.execute(
      """
      SELECT id, username, password_hash
      FROM users
      WHERE username = %s OR email = %s
      """,
      (identifier, identifier)
    )
    user = cursor.fetchone()

    if user is None:
        cursor.close()
        db.close()
        return jsonify({"msg": "Bad credentials"}), 401

    if not bcrypt.check_password_hash(user["password_hash"], password):
        cursor.close()
        db.close()
        return jsonify({"msg": "Bad credentials"}), 401

    token = create_access_token(
              identity=str(user["id"]),
              additional_claims={"username": user["username"]}
            )

    # Attach any guest cart items to this user
    cursor.execute("UPDATE cart_items SET user_id = %s WHERE user_id IS NULL", (user["id"],))
    db.commit()
    
    resp = jsonify({"access_token": token})
    resp.headers["Authorization"] = f"Bearer {token}"
    cursor.close()
    db.close()
    return resp, 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    db = get_db_connection()
    cursor = db.cursor()
    user_id = int(get_jwt_identity())
    cursor.execute(
        "SELECT id, username, points FROM users WHERE id=%s", (user_id,)
    )
    u = cursor.fetchone()
    cursor.close()
    db.close()
    if u is None:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(dict(u)), 200
