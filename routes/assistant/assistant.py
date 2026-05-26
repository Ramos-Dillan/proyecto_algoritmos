import os
from google import genai
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db.db import Sessionlocal
from db.models import Product, Category, TherapeuticGroup
from config import Config
from sqlalchemy import or_

assistant_bp = Blueprint('assistant', __name__)

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def get_vademecum_context(user_message):
    session = Sessionlocal()
    try:
        search = f"%{user_message}%"

        productos_relevantes = session.query(Product).filter(
            Product.is_active == True,
            or_(
                Product.commercial_name.ilike(search),
                Product.generic_name.ilike(search),
                Product.pharmaceutical_form.ilike(search),
                Product.dosage.ilike(search),
                Product.notes.ilike(search),
                Product.category.has(Category.name.ilike(search)),
                Product.therapeutic_group.has(TherapeuticGroup.name.ilike(search)),
                Product.therapeutic_group.has(TherapeuticGroup.description.ilike(search)),
                Product.therapeutic_group.has(TherapeuticGroup.mechanism.ilike(search)),
            )
        ).limit(20).all()

        # Busca por cada palabra individual si no encontró nada
        if not productos_relevantes:
            palabras = [p for p in user_message.split() if len(p) > 3]
            for palabra in palabras:
                s = f"%{palabra}%"
                resultado = session.query(Product).filter(
                    Product.is_active == True,
                    or_(
                        Product.commercial_name.ilike(s),
                        Product.generic_name.ilike(s),
                        Product.notes.ilike(s),
                        Product.category.has(Category.name.ilike(s)),
                        Product.therapeutic_group.has(TherapeuticGroup.name.ilike(s)),
                    )
                ).limit(20).all()
                if resultado:
                    productos_relevantes = resultado
                    break

        # Fallback final: manda todos para que Gemini decida
        if not productos_relevantes:
            productos_relevantes = session.query(Product).filter(
                Product.is_active == True
            ).all()

        context = "VADEMÉCUM OFTALMOLÓGICO CES - MEDICAMENTOS DISPONIBLES:\n\n"

        for p in productos_relevantes:
            context += (
                f"- {p.commercial_name} ({p.generic_name}) | "
                f"{p.concentration} | {p.pharmaceutical_form} | "
                f"Dosis: {p.dosage} | "
                f"Categoría: {p.category.name if p.category else 'N/A'} | "
                f"Grupo: {p.therapeutic_group.name if p.therapeutic_group else 'N/A'} | "
                f"Notas: {p.notes or 'N/A'}\n"
            )

        return context
    finally:
        session.close()

@assistant_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"status": "error", "message": "Mensaje vacío"}), 400

    try:
        vademecum = get_vademecum_context(user_message)

        prompt = f"""
Eres un asistente clínico oftalmológico especializado de la Universidad CES.
Tu función es ayudar a estudiantes y profesionales de optometría.

REGLAS:
1. Solo recomienda medicamentos que aparecen en el vademécum proporcionado
2. Si el usuario describe síntomas, sugiere posibles diagnósticos y medicamentos del vademécum
3. Si pregunta por un medicamento específico, explica para qué sirve, dosis y notas
4. Si pregunta por un diagnóstico, lista los medicamentos disponibles
5. Siempre incluye un aviso: "Esto es orientativo, consulta con tu oftalmólogo"
6. Responde siempre en español, sé conciso y claro
7. Respuestas cortas y directas, máximo 5 líneas

{vademecum}

PREGUNTA DEL USUARIO: {user_message}
"""

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({
            "status": "success",
            "data": {
                "response": response.text,
                "user_message": user_message
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@assistant_bp.route('/models', methods=['GET'])
@jwt_required()
def list_models():
    try:
        models = client.models.list()
        model_names = [m.name for m in models]
        return jsonify({"models": model_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500