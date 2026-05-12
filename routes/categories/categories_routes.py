from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from routes.categories import categories_controller

categories_bp = Blueprint("categories_bp", __name__)


@categories_bp.route("/getAll", methods=["GET"])
@jwt_required()
def getAll():
    return categories_controller.getAll()


@categories_bp.route("/createCategory", methods=["POST"])
@jwt_required()
def createCategory():
    data = request.json
    return categories_controller.createCategory(data)


@categories_bp.route("/deleteCategory/<int:id>", methods=["DELETE"])
@jwt_required()
def deleteCategory(id):
    return categories_controller.deleteCategory(id)


@categories_bp.route("/updateCategory/<int:id>", methods=["PUT"])
@jwt_required()
def updateCategory(id):
    data = request.get_json()
    return categories_controller.updateCategory(id, data)