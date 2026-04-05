from flask_jwt_extended import create_access_token
from common.http import ok, bad_request, unauthorized, created
from routes.auth import auth_service


def login_user(data):
    user, err = auth_service.login_user(data)

    if err:
        return unauthorized(message="Login inválido")

    token = create_access_token(identity=str(user.id))

    return ok(
        data={
            "access_token": token,
            "user": {
                "id": user.id,
                "username": getattr(user, "username", None),
                "identification": getattr(user, "identification", None)
            }
        },
        message="Login exitoso"
    )


def create_user(data):
    user, err = auth_service.create_user(data)

    if err:
        return bad_request(message="No se pudo crear el usuario", errors=err)

    return created(
        data={
            "id": user.id,
            "username": getattr(user, "username", None),
            "identification": getattr(user, "identification", None)
        },
        message="Usuario creado"
    )