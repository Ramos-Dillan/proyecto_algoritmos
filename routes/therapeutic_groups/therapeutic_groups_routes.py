from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from routes.therapeutic_groups import therapeutic_groups_controller

therapeutic_groups_bp = Blueprint("therapeutic_groups_bp", __name__)

@therapeutic_groups_bp.route("/getAll", methods=["GET"])
@jwt_required()
def getAll():
    return therapeutic_groups_controller.getAll()

@therapeutic_groups_bp.route("/createTherapeuticGroup", methods=["POST"])
@jwt_required()
def createTherapeuticGroup():
    data = request.json
    return therapeutic_groups_controller.createTherapeuticGroup(data)

@therapeutic_groups_bp.route("/deleteTherapeuticGroup/<int:id>", methods=["DELETE"])
@jwt_required()
def deleteTherapeuticGroup(id):
    return therapeutic_groups_controller.deleteTherapeuticGroup(id)

@therapeutic_groups_bp.route("/updateTherapeuticGroup/<int:id>", methods=["PUT"])
@jwt_required()
def updateTherapeuticGroup(id):
    data = request.get_json()
    return therapeutic_groups_controller.updateTherapeuticGroup(id, data)