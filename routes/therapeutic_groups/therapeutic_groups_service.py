from typing import List, Tuple, Any
from contextlib import contextmanager
from db.db import Sessionlocal
from db.models import TherapeuticGroup


@contextmanager
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def getAll() -> Tuple[List[TherapeuticGroup], Any]:
    try:
        with get_db() as db:
            groups = db.query(TherapeuticGroup).all()
            return groups, None
    except Exception as e:
        return None, str(e)


def createTherapeuticGroup(data):
    try:
        with get_db() as db:
            group = TherapeuticGroup(
                name=data.get("name"),
                mechanism=data.get("mechanism"),
                description=data.get("description")
            )

            db.add(group)
            db.commit()
            db.refresh(group)

            return group, None

    except Exception as e:
        return None, str(e)


def deleteTherapeuticGroup(id):
    try:
        with get_db() as db:
            group = db.query(TherapeuticGroup).filter(TherapeuticGroup.id == id).first()

            if not group:
                return False, "Therapeutic group not found"

            db.delete(group)
            db.commit()

            return True, None

    except Exception as e:
        return False, str(e)


def updateTherapeuticGroup(id: int, data):
    try:
        with get_db() as db:
            group = db.query(TherapeuticGroup).filter(TherapeuticGroup.id == id).first()

            if not group:
                return None, "Therapeutic group not found"

            group.name = data.get("name")
            group.mechanism = data.get("mechanism")
            group.description = data.get("description")

            db.commit()
            db.refresh(group)

            return group, None

    except Exception as e:
        return None, str(e)