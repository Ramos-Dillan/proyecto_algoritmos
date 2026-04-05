from typing import List, Tuple, Any
from contextlib import contextmanager
from db.db import Sessionlocal
from db.models import Laboratory


@contextmanager
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def getAll() -> Tuple[List[Laboratory], Any]:
    try:
        with get_db() as db:
            laboratories = db.query(Laboratory).all()
            return laboratories, None
    except Exception as e:
        return None, str(e)


def createLaboratory(data):
    try:
        name = (data.get("name") or "").strip()

        if not name:
            return None, "El nombre es requerido"

        with get_db() as db:
            # validar duplicados
            exists = db.query(Laboratory).filter(Laboratory.name == name).first()
            if exists:
                return None, "Ya existe un laboratorio con ese nombre"

            laboratory = Laboratory(name=name)

            db.add(laboratory)
            db.commit()
            db.refresh(laboratory)

            return laboratory, None

    except Exception as e:
        return None, str(e)


def deleteLaboratory(id):
    try:
        with get_db() as db:
            lab = db.query(Laboratory).filter(Laboratory.id == id).first()

            if not lab:
                return False, "Laboratorio no encontrado"

            db.delete(lab)
            db.commit()

            return True, None

    except Exception as e:
        return False, str(e)


def updateLaboratory(id: int, data):
    try:
        name = (data.get("name") or "").strip()

        if not name:
            return None, "El nombre es requerido"

        with get_db() as db:
            lab = db.query(Laboratory).filter(Laboratory.id == id).first()

            if not lab:
                return None, "Laboratorio no encontrado"

            lab.name = name

            db.commit()
            db.refresh(lab)

            return lab, None

    except Exception as e:
        return None, str(e)