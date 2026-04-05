from typing import List, Tuple, Any
from contextlib import contextmanager
from db.db import Sessionlocal
from db.models import Product


@contextmanager
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def getAll() -> Tuple[List[Product], Any]:
    try:
        with get_db() as db:
            products = db.query(Product).all()
            return products, None
    except Exception as e:
        return None, str(e)


def createProduct(data):
    try:
        with get_db() as db:
            product = Product(
                generic_name=data.get("generic_name"),
                commercial_name=data.get("commercial_name"),
                concentration=data.get("concentration"),
                pharmaceutical_form=data.get("pharmaceutical_form"),
                dosage=data.get("dosage"),
                notes=data.get("notes"),
                is_active=data.get("is_active", True),
                therapeutic_group_id=data.get("therapeutic_group_id"),
                laboratory_id=data.get("laboratory_id")
            )

            db.add(product)
            db.commit()
            db.refresh(product)

            return product, None

    except Exception as e:
        return None, str(e)


def deleteProduct(id):
    try:
        with get_db() as db:
            product = db.query(Product).filter(Product.id == id).first()

            if not product:
                return False, "Product not found"

            db.delete(product)
            db.commit()

            return True, None

    except Exception as e:
        return False, str(e)


def updateProduct(id: int, data):
    try:
        with get_db() as db:
            product = db.query(Product).filter(Product.id == id).first()

            if not product:
                return None, "Product not found"

            product.generic_name = data.get("generic_name")
            product.commercial_name = data.get("commercial_name")
            product.concentration = data.get("concentration")
            product.pharmaceutical_form = data.get("pharmaceutical_form")
            product.dosage = data.get("dosage")
            product.notes = data.get("notes")
            product.is_active = data.get("is_active")
            product.therapeutic_group_id = data.get("therapeutic_group_id")
            product.laboratory_id = data.get("laboratory_id")

            db.commit()
            db.refresh(product)

            return product, None

    except Exception as e:
        return None, str(e)