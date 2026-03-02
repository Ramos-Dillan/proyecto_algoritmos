from flask import Blueprint, request, jsonify
from database import db
from auth.controllers.auth_controller import register_controller, login_controller

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    response, status = register_controller(db.session, username, password)

    return jsonify(response), status
    