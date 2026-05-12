from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from security.roles import role_required   # 👈 IMPORTANTE

from routes.roles import roles_controller
from routes.auth import auth_controller

roles_bp = Blueprint("roles_bp", __name__)

# 🔥 CREAR ROL (solo admin)
@roles_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["admin"])
def create_role():
    data = request.get_json()
    return roles_controller.createRole(data)


# 🔥 OBTENER ROLES (admin o medico)
@roles_bp.route("/roles", methods=["GET"])
@jwt_required()
@role_required(["admin", "medico"])
def get_roles():
    return roles_controller.getAll()


# 🔥 OBTENER USUARIOS (solo admin)
@roles_bp.route("/users", methods=["GET"])
@jwt_required()
@role_required(["admin"])
def get_users():
    return auth_controller.get_users()