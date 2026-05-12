from typing import List, Tuple, Any
from contextlib import contextmanager
from db.db import Sessionlocal
from db.models import Category


@contextmanager
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def getAll() -> Tuple[List[Category], Any]:
    try:
        with get_db() as db:
            categories = db.query(Category).all()
            return categories, None
    except Exception as e:
        return None, str(e)


def createCategory(data):
    try:
        name = (data.get("name") or "").strip()

        if not name:
            return None, "El nombre es requerido"

        with get_db() as db:
            exists = db.query(Category).filter(Category.name == name).first()
            if exists:
                return None, "Ya existe una categoría con ese nombre"

            category = Category(name=name)

            db.add(category)
            db.commit()
            db.refresh(category)

            return category, None

    except Exception as e:
        return None, str(e)


def deleteCategory(id):
    try:
        with get_db() as db:
            category = db.query(Category).filter(Category.id == id).first()

            if not category:
                return False, "Categoría no encontrada"

            db.delete(category)
            db.commit()

            return True, None

    except Exception as e:
        return False, str(e)


def updateCategory(id: int, data):
    try:
        name = (data.get("name") or "").strip()

        if not name:
            return None, "El nombre es requerido"

        with get_db() as db:
            category = db.query(Category).filter(Category.id == id).first()

            if not category:
                return None, "Categoría no encontrada"

            category.name = name

            db.commit()
            db.refresh(category)

            return category, None

    except Exception as e:
        return None, str(e)