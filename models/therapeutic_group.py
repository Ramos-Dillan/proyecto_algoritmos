from database import db

class TherapeuticGroup(db.Model):
    __tablename__ = "therapeutic_groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    mechanism = db.Column(db.Text)
    description = db.Column(db.Text)

    products = db.relationship("Product", backref="therapeutic_group", lazy=True)