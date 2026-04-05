from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from routes.laboratories import laboratories_controller

laboratories_bp = Blueprint("laboratories_bp", __name__)

@laboratories_bp.route("/getAll", methods=["GET"])
@jwt_required()
def getAll():
    return laboratories_controller.getAll()


@laboratories_bp.route("/createLaboratory", methods=["POST"])
@jwt_required()
def createLaboratory():
    data = request.json
    return laboratories_controller.createLaboratory(data)


@laboratories_bp.route("/deleteLaboratory/<int:id>", methods=["DELETE"])
@jwt_required()
def deleteLaboratory(id):
    return laboratories_controller.deleteLaboratory(id)


@laboratories_bp.route("/updateLaboratory/<int:id>", methods=["PUT"])
@jwt_required()
def updateLaboratory(id):
    data = request.get_json()
    return laboratories_controller.updateLaboratory(id, data)