from flask import Blueprint, request
from routes.assistant.assistant_controller import chat
from flask_jwt_extended import jwt_required

assistant_bp = Blueprint("assistant_bp", __name__)

@assistant_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat_route():
    data = request.get_json() or {}
    return chat(data)