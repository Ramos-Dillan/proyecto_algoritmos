from flask import Blueprint
from flask_jwt_extended import jwt_required
from routes.dashboard.dashboard_controller import get_summary

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    return get_summary()