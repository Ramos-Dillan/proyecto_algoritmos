from contextlib import contextmanager
from db.db import Sessionlocal
from db.models import User, Product, Laboratory, TherapeuticGroup, Category


@contextmanager
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def get_summary():
    try:
        with get_db() as db:

            # 🔢 TOTALES
            total_users = db.query(User).count()
            total_products = db.query(Product).count()
            total_labs = db.query(Laboratory).count()
            total_groups = db.query(TherapeuticGroup).count()
            total_categories = db.query(Category).count()

            # 📊 ACTIVOS / INACTIVOS
            active_products = db.query(Product).filter(Product.is_active == True).count()
            inactive_products = total_products - active_products

            # 📊 PRODUCTOS POR GRUPO
            groups_data = db.query(
                TherapeuticGroup.name,
                Product.id
            ).join(Product).all()

            groups_dict = {}

            for g in groups_data:
                groups_dict[g[0]] = groups_dict.get(g[0], 0) + 1

            # 📊 PRODUCTOS POR CATEGORÍA
            categories_data = db.query(
                Category.name,
                Product.id
            ).join(Product).all()

            categories_dict = {}

            for c in categories_data:
                categories_dict[c[0]] = categories_dict.get(c[0], 0) + 1

            return {
                "totalUsers": total_users,
                "totalProducts": total_products,
                "totalLabs": total_labs,
                "totalGroups": total_groups,
                "totalCategories": total_categories,

                "activeProducts": active_products,
                "inactiveProducts": inactive_products,

                "chart": {
                    "groups": list(groups_dict.keys()),
                    "products": list(groups_dict.values())
                },

                "categoriesChart": {
                    "categories": list(categories_dict.keys()),
                    "products": list(categories_dict.values())
                }

            }, None

    except Exception as e:
        return None, str(e)