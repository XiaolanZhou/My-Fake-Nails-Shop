import sys
import os

# Add server directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

app = Flask(__name__)

# Use environment variables for secrets
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-key")

# Allow both localhost (dev) and Vercel (prod)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "https://my-fake-nails-shop.vercel.app",
            os.getenv("FRONTEND_URL", "")
        ]
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
