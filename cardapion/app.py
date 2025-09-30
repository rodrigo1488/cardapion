from flask import Flask, render_template, request, jsonify, session
import os



app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


def register_blueprints():
    from routes.company import company_bp
    from routes.users import users_bp
    from routes.auth import auth_bp
    from routes.delivery import delivery_bp
    from routes.categories import categories_bp
    from routes.products import products_bp
    from routes.orders import orders_bp

    app.register_blueprint(company_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)



if __name__ == "__main__":
    register_blueprints()
    app.run(debug=True, host="0.0.0.0", port=5000)

