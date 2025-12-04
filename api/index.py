import sys
import os

# Add server directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from flask import Flask, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

app = Flask(__name__)

# Use environment variables for secrets
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-key")

# Allow localhost (dev), Vercel preview, and custom domains
allowed_origins = [
    "http://localhost:5173",
    "https://my-fake-nails-shop.vercel.app",
    "https://meowoem.com",
    "https://www.meowoem.com",
]
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins
    }
})
app.url_map.strict_slashes = False

bcrypt.init_app(app)
jwt.init_app(app)

# Import and register blueprints
from app.routes.products import products_bp
from app.routes.cart import cart_bp
from app.routes.orders import orders_bp
from app.routes.users import users_bp
from app.routes.auth import auth_bp
from app.routes.payments import payments_bp
from app.routes.uploads import uploads_bp

app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(payments_bp, url_prefix='/api/payments')
app.register_blueprint(uploads_bp, url_prefix='/api/uploads')

# Health check
@app.route('/api/health')
def health():
    return {"status": "ok"}

# Debug endpoint to test database
@app.route('/api/debug')
def debug():
    try:
        db_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
        has_db_url = bool(db_url)
        
        # Try to connect
        from app.db import get_db_connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as count FROM products")
        row = cur.fetchone()
        count = row['count'] if row else 0
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "ok",
            "has_database_url": has_db_url,
            "product_count": count
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "has_database_url": bool(os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL"))
        }), 500
