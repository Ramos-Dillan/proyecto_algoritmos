from typing import List, Tuple, Any
from contextlib import contextmanager
from db.db import Sessionlocal
from db.models import Role


@contextmanager
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 OBTENER ROLES
def getAll() -> Tuple[List[Role], Any]:
    try:
        with get_db() as db:
            roles = db.query(Role).all()
            return roles, None
    except Exception as e:
        return None, str(e)


# 🔥 CREAR ROL (OPCIONAL)
def createRole(data):
    try:
        name = (data.get("name") or "").strip()

        if not name:
            return None, "El nombre es requerido"

        with get_db() as db:
            exists = db.query(Role).filter(Role.name == name).first()
            if exists:
                return None, "El rol ya existe"

            role = Role(name=name)

            db.add(role)
            db.commit()
            db.refresh(role)

            return role, None

    except Exception as e:
        return None, str(e)