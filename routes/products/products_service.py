from typing import List, Tuple, Any
from contextlib import contextmanager
from db.db import Sessionlocal
from db.models import Product
from sqlalchemy.orm import joinedload

@contextmanager
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def getAll():
    try:
        with get_db() as db:
            products = db.query(Product)\
                .options(
                    joinedload(Product.therapeutic_group),
                    joinedload(Product.laboratory),
                    joinedload(Product.category)
                )\
                .order_by(Product.id)\
                .all()
            return [p.to_dict() for p in products], None
    except Exception as e:
        return None, str(e)


def getById(id: int):
    try:
        with get_db() as db:
            product = db.query(Product)\
                .options(
                    joinedload(Product.therapeutic_group),
                    joinedload(Product.laboratory),
                    joinedload(Product.category)
                )\
                .filter(Product.id == id).first()
            if not product:
                return None, "Product not found"
            return product.to_dict(), None
    except Exception as e:
        return None, str(e)


def filterProducts(params: dict):
    try:
        page = int(params.get('page', 1))
        per_page = int(params.get('per_page', 20))
    except Exception:
        page = 1
        per_page = 20

    try:
        with get_db() as db:
            query = db.query(Product)\
                .options(
                    joinedload(Product.therapeutic_group),
                    joinedload(Product.laboratory),
                    joinedload(Product.category)
                )\
                .order_by(Product.id)

            if 'search' in params and params.get('search'):
                s = f"%{params.get('search')}%"
                query = query.filter(
                    (Product.generic_name.ilike(s)) |
                    (Product.commercial_name.ilike(s))
                )

            if params.get('category_id'):
                query = query.filter(Product.category_id == int(params.get('category_id')))

            if params.get('therapeutic_group_id'):
                query = query.filter(Product.therapeutic_group_id == int(params.get('therapeutic_group_id')))

            if params.get('laboratory_id'):
                query = query.filter(Product.laboratory_id == int(params.get('laboratory_id')))

            if params.get('is_active') is not None:
                val = params.get('is_active')
                if isinstance(val, str):
                    val = val.lower() in ['1', 'true', 'yes']
                query = query.filter(Product.is_active == bool(val))

            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return [p.to_dict() for p in items], total, None
    except Exception as e:
        return None, 0, str(e)


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
            product = db.query(Product)\
                .options(
                    joinedload(Product.therapeutic_group),
                    joinedload(Product.laboratory),
                    joinedload(Product.category)
                )\
                .filter(Product.id == id).first()
            if not product:
                return None, "Product not found"
            product.generic_name = data.get("generic_name")
            product.commercial_name = data.get("commercial_name")
            product.concentration = data.get("concentration")
            product.pharmaceutical_form = data.get("pharmaceutical_form")
            product.dosage = data.get("dosage")
            product.notes = data.get("notes")
            product.is_active = data.get("is_active", product.is_active)
            if data.get("therapeutic_group_id") is not None:
                product.therapeutic_group_id = data.get("therapeutic_group_id")
            if data.get("laboratory_id") is not None:
                product.laboratory_id = data.get("laboratory_id")
            if data.get("image_url") is not None:
                product.image_url = data.get("image_url")
            db.commit()
            db.refresh(product)
            return product.to_dict(), None  # ✅ adentro del with
    except Exception as e:
        return None, str(e)


def toggleActive(id: int, is_active: bool):
    try:
        with get_db() as db:
            product = db.query(Product)\
                .options(
                    joinedload(Product.therapeutic_group),
                    joinedload(Product.laboratory),
                    joinedload(Product.category)
                )\
                .filter(Product.id == id).first()
            if not product:
                return None, "Product not found"
            product.is_active = is_active
            db.commit()
            db.refresh(product)
            return product.to_dict(), None  # ✅ adentro del with
    except Exception as e:
        return None, str(e)