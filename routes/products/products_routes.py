from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from routes.products import products_controller

products_bp = Blueprint("products_bp", __name__)

@products_bp.route("/getAll", methods=["GET"])
@jwt_required()
def getAll():
    return products_controller.getAll()

@products_bp.route("/createProduct", methods=["POST"])
@jwt_required()
def createProduct():
    data = request.json
    return products_controller.createProduct(data)

@products_bp.route("/deleteProduct/<int:id>", methods=["DELETE"])
@jwt_required()
def deleteProduct(id):
    return products_controller.deleteProduct(id)

@products_bp.route("/updateProduct/<int:id>", methods=["PUT"])
@jwt_required()
def updateProduct(id):
    data = request.get_json()
    return products_controller.updateProduct(id, data)