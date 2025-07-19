from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt    = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "veryevrueSeCRETlkauwexyvskty"

    # allow ONLY your Vite dev server to hit any /api/* URL
    CORS(app, resources={
      r"/api/*": {
        "origins": "http://localhost:5173"
      }
    })
    app.url_map.strict_slashes = False

    bcrypt.init_app(app)
    jwt.init_app(app)

    # register your blueprints
    from app.routes.products import products_bp
    from app.routes.cart     import cart_bp
    from app.routes.orders   import orders_bp
    from app.routes.users    import users_bp
    from app.routes.auth     import auth_bp

    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(cart_bp,     url_prefix='/api/cart')
    app.register_blueprint(orders_bp,   url_prefix='/api/orders')
    app.register_blueprint(users_bp,    url_prefix='/api/users')
    app.register_blueprint(auth_bp,     url_prefix="/api/auth")

    return app
