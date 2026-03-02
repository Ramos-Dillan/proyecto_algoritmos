from sqlalchemy.orm import Session
from auth.services.auth_service import register_user, authenticate_user
from auth.auth_handler import create_access_token


def register_controller(db: Session, username: str, password: str):
    user = register_user(db, username, password)

    if not user:
        return {"error": "El usuario ya existe"}, 400

    token = create_access_token({"sub": user.username})

    return {
        "message": "Usuario creado correctamente",
        "access_token": token,
        "token_type": "bearer"
    }, 201


def login_controller(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)

    if not user:
        return {"error": "Credenciales incorrectas"}, 401

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }, 200