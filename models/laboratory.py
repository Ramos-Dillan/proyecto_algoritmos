from database import db

class Laboratory(db.Model):
    __tablename__ = "laboratories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)

    products = db.relationship("Product", backref="laboratory", lazy=True)