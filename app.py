from flask import Flask
from config import Config
from database import db

# Models
from models.therapeutic_group import TherapeuticGroup
from models.laboratory import Laboratory
from models.product import Product
from models.user import User  

# Routes
from routes.therapeutic_group_routes import therapeutic_group_bp
from routes.product_routes import product_bp
from routes.laboratory_routes import laboratory_bp

# 🔐 Auth Blueprint
from auth.routes.auth_routes import auth_bp  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Blueprints
    app.register_blueprint(therapeutic_group_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(laboratory_bp)
    app.register_blueprint(auth_bp)  

    @app.route("/")
    def home():
        return {"message": "Servidor funcionando correctamente 🚀"}

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea también la tabla users
    app.run(debug=True)