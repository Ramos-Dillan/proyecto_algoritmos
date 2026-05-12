from db.db import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey,DateTime
from sqlalchemy.orm import relationship


# =========================
# 🏥 LABORATORY
# =========================
class Laboratory(Base):
    __tablename__ = "laboratories"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)

    products = relationship("Product", back_populates="laboratory")


# =========================
# 💊 THERAPEUTIC GROUP
# =========================
class TherapeuticGroup(Base):
    __tablename__ = "therapeutic_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    mechanism = Column(Text)
    description = Column(Text)

    products = relationship("Product", back_populates="therapeutic_group")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mechanism": self.mechanism,
            "description": self.description
        }


# =========================
# 🗂️ CATEGORY
# =========================
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)

    products = relationship("Product", back_populates="category")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


# =========================
# 📦 PRODUCT
# =========================
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    generic_name = Column(String(150))
    commercial_name = Column(String(150))
    concentration = Column(String(50))
    pharmaceutical_form = Column(String(100))
    dosage = Column(Text)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    image_url = Column(String(500), nullable=True)  # ✅ nuevo

    # 🔗 RELACIONES
    therapeutic_group_id = Column(
        Integer,
        ForeignKey("therapeutic_groups.id"),
        nullable=False
    )

    laboratory_id = Column(
        Integer,
        ForeignKey("laboratories.id"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    # 🔗 ORM RELATIONSHIPS
    therapeutic_group = relationship("TherapeuticGroup", back_populates="products")
    laboratory = relationship("Laboratory", back_populates="products")
    category = relationship("Category", back_populates="products")

    def to_dict(self):
        return {
            "id": self.id,
            "generic_name": self.generic_name,
            "commercial_name": self.commercial_name,
            "concentration": self.concentration,
            "pharmaceutical_form": self.pharmaceutical_form,
            "dosage": self.dosage,
            "notes": self.notes,
            "is_active": self.is_active,
            "image_url": self.image_url,  # ✅ nuevo

            "therapeutic_group": self.therapeutic_group.name if self.therapeutic_group else None,
            "laboratory": self.laboratory.name if self.laboratory else None,
            "category": self.category.name if self.category else None
        }


# =========================
# 👤 USER
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    identification = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    reset_token = Column(String(255), nullable=True, index=True)
    reset_token_expires = Column(DateTime, nullable=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users")

    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "identification": self.identification,
            "role": self.role.name if self.role else None
        }


# =========================
# 👤 ROLE
# =========================
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")