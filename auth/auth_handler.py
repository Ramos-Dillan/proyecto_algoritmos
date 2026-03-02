from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from flask import request, jsonify
from functools import wraps
from config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔐 Hash contraseña
def hash_password(password: str):
    password = password[:72]  # bcrypt límite real
    return pwd_context.hash(password)


# 🔎 Verificar contraseña
def verify_password(plain: str, hashed: str):
    plain = plain[:72]
    return pwd_context.verify(plain, hashed)


# 🎟 Crear token
def create_access_token(data: dict):
    expiration = datetime.utcnow() + timedelta(
        minutes=Config.JWT_EXPIRATION_MINUTES
    )

    payload = data.copy()
    payload.update({
        "exp": expiration
    })

    return jwt.encode(
        payload,
        Config.SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )


# 🛡 Decorador para proteger rutas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 📌 Espera: Authorization: Bearer <token>
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Token requerido"}), 401

        try:
            data = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=[Config.JWT_ALGORITHM]
            )

            current_user = data.get("sub")

        except JWTError:
            return jsonify({"message": "Token inválido o expirado"}), 401

        # 🔥 Pasa el username al endpoint
        return f(current_user, *args, **kwargs)

    return decorated