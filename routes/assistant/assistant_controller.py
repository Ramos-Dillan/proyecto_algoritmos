from routes.assistant.assistant_service import get_chat_response
from common.http import ok, bad_request

def chat(data):
    message = (data.get("message") or "").strip()

    if not message:
        return bad_request(message="Mensaje vacío")

    response, err = get_chat_response(message)

    if err:
        return bad_request(message=err["message"])

    return ok(data=response, message="Respuesta generada correctamente")