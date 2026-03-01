from flask import Blueprint, request
from models.therapeutic_group import TherapeuticGroup
from database import db
from utils.http_response import success_response, error_response

therapeutic_group_bp = Blueprint("therapeutic_group_bp", __name__)


# 🔹 Crear grupo terapéutico
@therapeutic_group_bp.route("/therapeutic-groups", methods=["POST"])
def create_therapeutic_group():
    data = request.get_json()

    if not data or not data.get("name"):
        return error_response("El nombre es obligatorio", 400)

    new_group = TherapeuticGroup(
        name=data["name"],
        mechanism=data.get("mechanism"),
        description=data.get("description")
    )

    db.session.add(new_group)
    db.session.commit()

    return success_response(
        {
            "id": new_group.id,
            "name": new_group.name
        },
        "Grupo terapéutico creado",
        201
    )


# 🔹 Obtener todos
@therapeutic_group_bp.route("/therapeutic-groups", methods=["GET"])
def get_therapeutic_groups():
    groups = TherapeuticGroup.query.all()

    result = [
        {
            "id": g.id,
            "name": g.name,
            "mechanism": g.mechanism,
            "description": g.description
        }
        for g in groups
    ]

    return success_response(result, "Lista de grupos")

# 🔹 Actualizar grupo terapéutico
@therapeutic_group_bp.route("/therapeutic-groups/<int:id>", methods=["PUT"])
def update_therapeutic_group(id):
    data = request.get_json()
    group = TherapeuticGroup.query.get(id)

    if not group:
        return error_response("Grupo terapéutico no encontrado", 404)

    group.name = data.get("name", group.name)
    group.mechanism = data.get("mechanism", group.mechanism)
    group.description = data.get("description", group.description)

    db.session.commit()

    return success_response(
        {
            "id": group.id,
            "name": group.name,
            "mechanism": group.mechanism,
            "description": group.description
        },
        "Grupo terapéutico actualizado"
    )


# 🔹 Borrar grupo terapéutico
@therapeutic_group_bp.route("/therapeutic-groups/<int:id>", methods=["DELETE"])
def delete_therapeutic_group(id):
    group = TherapeuticGroup.query.get(id)

    if not group:
        return error_response("Grupo terapéutico no encontrado", 404)

    db.session.delete(group)
    db.session.commit()

    return success_response({"id": id}, "Grupo terapéutico eliminado")