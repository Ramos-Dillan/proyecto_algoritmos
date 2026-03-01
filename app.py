from flask import Flask
from config import Config
from database import db

# Models
from models.therapeutic_group import TherapeuticGroup
from models.laboratory import Laboratory
from models.product import Product

# Routes
from routes.therapeutic_group_routes import therapeutic_group_bp
from routes.product_routes import product_bp

#Laboratory
from routes.laboratory_routes import laboratory_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Blueprints
    app.register_blueprint(therapeutic_group_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(laboratory_bp)

    @app.route("/")
    def home():
        return {"message": "Servidor funcionando correctamente 🚀"}

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)