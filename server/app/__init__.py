from flask import Flask
from flask_cors import CORS
from app.routes.products import products_bp
from app.routes.cart import cart_bp
from app.routes.orders import orders_bp
from app.routes.users import users_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    return app
