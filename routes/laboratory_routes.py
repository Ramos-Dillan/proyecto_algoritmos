from flask import Blueprint, request, jsonify
from models.laboratory import Laboratory
from database import db

laboratory_bp = Blueprint("laboratory_bp", __name__, url_prefix="/laboratories")


# ==============================
# CREAR LABORATORIO
# ==============================
@laboratory_bp.route("/", methods=["POST"])
def create_laboratory():
    data = request.get_json()

    try:
        new_laboratory = Laboratory(
            name=data["name"]
        )

        db.session.add(new_laboratory)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Laboratorio creado correctamente",
            "data": {
                "id": new_laboratory.id,
                "name": new_laboratory.name
            }
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


# ==============================
# OBTENER TODOS
# ==============================
@laboratory_bp.route("/", methods=["GET"])
def get_laboratories():
    laboratories = Laboratory.query.all()

    result = []
    for lab in laboratories:
        result.append({
            "id": lab.id,
            "name": lab.name
        })

    return jsonify({
        "success": True,
        "data": result
    }), 200


# ==============================
# OBTENER POR ID
# ==============================
@laboratory_bp.route("/<int:id>", methods=["GET"])
def get_laboratory(id):
    lab = Laboratory.query.get(id)

    if not lab:
        return jsonify({
            "success": False,
            "message": "Laboratorio no encontrado"
        }), 404

    return jsonify({
        "success": True,
        "data": {
            "id": lab.id,
            "name": lab.name
        }
    }), 200


# ==============================
# ACTUALIZAR
# ==============================
@laboratory_bp.route("/<int:id>", methods=["PUT"])
def update_laboratory(id):
    lab = Laboratory.query.get(id)

    if not lab:
        return jsonify({
            "success": False,
            "message": "Laboratorio no encontrado"
        }), 404

    data = request.get_json()

    lab.name = data.get("name", lab.name)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Laboratorio actualizado correctamente"
    }), 200


# ==============================
# ELIMINAR
# ==============================
@laboratory_bp.route("/<int:id>", methods=["DELETE"])
def delete_laboratory(id):
    lab = Laboratory.query.get(id)

    if not lab:
        return jsonify({
            "success": False,
            "message": "Laboratorio no encontrado"
        }), 404

    db.session.delete(lab)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Laboratorio eliminado correctamente"
    }), 200