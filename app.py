from flask import Flask, request as flask_request
from config import Config

from db.db import engine
from db.models import Base

from routes.auth.auth_routes import auth_bp
from routes.laboratories.laboratories_routes import laboratories_bp
from routes.products.products_routes import products_bp
from routes.therapeutic_groups.therapeutic_groups_routes import therapeutic_groups_bp
from routes.roles.roles_routes import roles_bp
from routes.dashboard.dashboard_routes import dashboard_bp
from routes.categories.categories_routes import categories_bp
from routes.assistant.assistant_routes import assistant_bp

from flask_cors import CORS
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ CORS corregido
    CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],  # ✅ agrega PATCH
    supports_credentials=True
)
    
    @app.before_request
    def handle_options():
        if flask_request.method == "OPTIONS":
            return {}, 200

    # 🔥 JWT
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return {"message": "Token requerido"}, 401

    @jwt.invalid_token_loader
    def invalid_token_response(callback):
        return {"message": "Token inválido"}, 401

    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        return {"message": "Token expirado"}, 401

    # 🔥 RUTAS
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(laboratories_bp, url_prefix="/laboratory")
    app.register_blueprint(products_bp, url_prefix="/product")
    app.register_blueprint(therapeutic_groups_bp, url_prefix="/therapeutic_group")
    app.register_blueprint(roles_bp, url_prefix="/role")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(categories_bp, url_prefix="/categories")
    app.register_blueprint(assistant_bp, url_prefix='/assistant')

    @app.route("/")
    def home():
        return {"message": "API Vademecum funcionando 🚀"}

    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Ruta no encontrada"}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {"message": "Error interno del servidor"}, 500

    return app


app = create_app()

if __name__ == "__main__":
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos conectada y tablas creadas")
    except Exception as e:
        print("❌ Error conectando a la DB:", e)

    print("🚀 Servidor corriendo en http://localhost:5000")
    app.run(debug=True)
