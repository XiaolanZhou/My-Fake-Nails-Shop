from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # allow ONLY your Vite dev server to hit any /api/* URL
    CORS(app, resources={
      r"/api/*": {
        "origins": "http://localhost:5173"
      }
    })

    # turn off strict-slashes so /api/products and /api/products/ both work
    app.url_map.strict_slashes = False

    # register your blueprints
    from app.routes.products import products_bp
    from app.routes.cart     import cart_bp
    from app.routes.orders   import orders_bp
    from app.routes.users    import users_bp

    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(cart_bp,     url_prefix='/api/cart')
    app.register_blueprint(orders_bp,   url_prefix='/api/orders')
    app.register_blueprint(users_bp,    url_prefix='/api/users')

    return app
