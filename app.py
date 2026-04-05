from flask import Flask
from config import Config
# DB
from db.db import engine
from db.models import Base

# BLUEPRINTS
from routes.auth.auth_routes import auth_bp
from routes.laboratories.laboratories_routes import laboratories_bp
from routes.products.products_routes import products_bp
from routes.therapeutic_groups.therapeutic_groups_routes import therapeutic_groups_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    from flask_jwt_extended import JWTManager
    JWTManager(app)

    # 🔗 BLUEPRINTS
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(laboratories_bp, url_prefix="/laboratory")
    app.register_blueprint(products_bp, url_prefix="/product")
    app.register_blueprint(therapeutic_groups_bp, url_prefix="/therapeutic_group")


    @app.route("/")
    def home():
        return {"message": "API Vademecum funcionando 🚀"}

    return app


app = create_app()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    app.run(debug=True)