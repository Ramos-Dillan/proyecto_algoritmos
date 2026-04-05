from typing import Any, Tuple, Dict, Optional
from contextlib import contextmanager
from db.db import Sessionlocal
from db.models import User
from werkzeug.security import check_password_hash, generate_password_hash


@contextmanager
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 LOGIN
def login_user(data) -> Tuple[Optional[User], Any]:
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not password:
        return None, {"message": "Username y password son requeridos"}

    with get_db() as db:
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return None, {"message": "Usuario no encontrado"}

        if not check_password_hash(user.password, password):
            return None, {"message": "Password incorrecto"}

        return user, None


# 👤 REGISTER
def create_user(data: Dict[str, Any]) -> Tuple[Optional[User], Any]:
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not password:
        return None, {"message": "Username y password son requeridos"}

    with get_db() as db:
        exists = db.query(User).filter(User.username == username).first()

        if exists:
            return None, {"message": "Ya existe un usuario con ese username"}

        user = User(
            username=username,
            password=generate_password_hash(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user, None