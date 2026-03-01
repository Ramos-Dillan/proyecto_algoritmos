from flask import Blueprint, request, jsonify
from models.product import Product
from database import db

product_bp = Blueprint("product_bp", __name__, url_prefix="/products")


# ==============================
# CREAR PRODUCTO
# ==============================
@product_bp.route("/", methods=["POST"])
def create_product():
    data = request.get_json()

    try:
        new_product = Product(
            generic_name=data["generic_name"],
            commercial_name=data["commercial_name"],
            concentration=data["concentration"],
            pharmaceutical_form=data["pharmaceutical_form"],
            dosage=data["dosage"],
            notes=data.get("notes"),
            is_active=data.get("is_active", True),
            therapeutic_group_id=data["therapeutic_group_id"],
            laboratory_id=data["laboratory_id"]
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Producto creado correctamente",
            "data": {
                "id": new_product.id,
                "generic_name": new_product.generic_name,
                "commercial_name": new_product.commercial_name
            }
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


# ==============================
# OBTENER TODOS LOS PRODUCTOS
# ==============================
@product_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()

    result = []
    for product in products:
        result.append({
            "id": product.id,
            "generic_name": product.generic_name,
            "commercial_name": product.commercial_name,
            "concentration": product.concentration,
            "pharmaceutical_form": product.pharmaceutical_form,
            "dosage": product.dosage,
            "notes": product.notes,
            "is_active": product.is_active,
            "therapeutic_group_id": product.therapeutic_group_id,
            "laboratory_id": product.laboratory_id
        })

    return jsonify({
        "success": True,
        "data": result
    }), 200


# ==============================
# OBTENER PRODUCTO POR ID
# ==============================
@product_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({
            "success": False,
            "message": "Producto no encontrado"
        }), 404

    return jsonify({
        "success": True,
        "data": {
            "id": product.id,
            "generic_name": product.generic_name,
            "commercial_name": product.commercial_name,
            "concentration": product.concentration,
            "pharmaceutical_form": product.pharmaceutical_form,
            "dosage": product.dosage,
            "notes": product.notes,
            "is_active": product.is_active,
            "therapeutic_group_id": product.therapeutic_group_id,
            "laboratory_id": product.laboratory_id
        }
    }), 200


# ==============================
# ACTUALIZAR PRODUCTO
# ==============================
@product_bp.route("/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({
            "success": False,
            "message": "Producto no encontrado"
        }), 404

    data = request.get_json()

    product.generic_name = data.get("generic_name", product.generic_name)
    product.commercial_name = data.get("commercial_name", product.commercial_name)
    product.concentration = data.get("concentration", product.concentration)
    product.pharmaceutical_form = data.get("pharmaceutical_form", product.pharmaceutical_form)
    product.dosage = data.get("dosage", product.dosage)
    product.notes = data.get("notes", product.notes)
    product.is_active = data.get("is_active", product.is_active)
    product.therapeutic_group_id = data.get("therapeutic_group_id", product.therapeutic_group_id)
    product.laboratory_id = data.get("laboratory_id", product.laboratory_id)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Producto actualizado correctamente"
    }), 200


# ==============================
# ELIMINAR PRODUCTO
# ==============================
@product_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({
            "success": False,
            "message": "Producto no encontrado"
        }), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Producto eliminado correctamente"
    }), 200