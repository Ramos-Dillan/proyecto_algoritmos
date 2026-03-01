from database import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    generic_name = db.Column(db.String(150))
    commercial_name = db.Column(db.String(150))
    concentration = db.Column(db.String(50))
    pharmaceutical_form = db.Column(db.String(100))
    dosage = db.Column(db.Text)
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    therapeutic_group_id = db.Column(
        db.Integer,
        db.ForeignKey("therapeutic_groups.id"),
        nullable=False
    )

    laboratory_id = db.Column(
        db.Integer,
        db.ForeignKey("laboratories.id"),
        nullable=False
    )