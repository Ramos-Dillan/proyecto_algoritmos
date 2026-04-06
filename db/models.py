from db.db import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
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
            "therapeutic_group_id": self.therapeutic_group_id,
            "laboratory_id": self.laboratory_id
        }

    # 🔗 Relaciones inversas
    therapeutic_group = relationship("TherapeuticGroup", back_populates="products")
    laboratory = relationship("Laboratory", back_populates="products")


# =========================
# 👤 USER
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)