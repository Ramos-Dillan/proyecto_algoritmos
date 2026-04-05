from flask import Blueprint, request
from routes.auth import auth_controller

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/create", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    return auth_controller.create_user(data)

@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json() or {}
    return auth_controller.login_user(data)