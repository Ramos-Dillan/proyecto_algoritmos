from google import genai
from config import Config
from db.db import Sessionlocal
from sqlalchemy import text

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def get_vademecum_context(user_message):
    try:
        db = Sessionlocal()

        # Trae TODO el vademécum para que Gemini tenga contexto completo
        result = db.execute(text("""
            SELECT p.generic_name, p.commercial_name, p.concentration,
                   p.pharmaceutical_form, p.dosage, p.notes,
                   tg.name as therapeutic_group, tg.mechanism, tg.description as tg_description,
                   l.name as laboratory, c.name as category
            FROM products p
            LEFT JOIN therapeutic_groups tg ON p.therapeutic_group_id = tg.id
            LEFT JOIN laboratories l ON p.laboratory_id = l.id
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.is_active = true
            ORDER BY p.generic_name
        """))

        rows = result.fetchall()
        db.close()

        if not rows:
            return "El vademécum está vacío."

        resultado = "VADEMÉCUM COMPLETO DISPONIBLE:\n"
        for row in rows:
            resultado += (
                f"- {row.commercial_name} | Genérico: {row.generic_name} | "
                f"Concentración: {row.concentration} | Forma: {row.pharmaceutical_form} | "
                f"Dosis: {row.dosage} | Notas: {row.notes} | "
                f"Grupo terapéutico: {row.therapeutic_group} | "
                f"Mecanismo: {row.mechanism} | Categoría: {row.category} | "
                f"Laboratorio: {row.laboratory}\n"
            )

        return resultado

    except Exception as e:
        return f"Error consultando vademécum: {str(e)}"


def get_chat_response(user_message):
    try:
        vademecum = get_vademecum_context(user_message)

        prompt = f"""
Eres un asistente clínico oftalmológico especializado de la Universidad CES.
Tu función es ayudar a estudiantes y profesionales de optometría.

Tienes acceso al vademécum completo de la institución. Úsalo para responder.

REGLAS ESTRICTAS:
1. Solo menciona medicamentos que aparezcan EXACTAMENTE en el vademécum proporcionado
2. Si el usuario describe síntomas, sugiere posibles diagnósticos y los medicamentos del vademécum
3. Si pregunta por un medicamento específico (por nombre genérico o comercial), explica para qué sirve, dosis y notas
4. Si pregunta por un diagnóstico o grupo terapéutico, lista los medicamentos disponibles
5. Si el medicamento NO está en el vademécum, dilo claramente
6. Siempre termina con: "⚠️ Esto es orientativo, consulta con tu oftalmólogo"
7. Responde siempre en español, sé conciso y claro
8. Máximo 6 líneas de respuesta

{vademecum}

PREGUNTA DEL USUARIO: {user_message}
"""

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        return {
            "response": response.text,
            "user_message": user_message
        }, None

    except Exception as e:
        return None, {"message": str(e)}