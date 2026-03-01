from models.laboratory import Laboratory
from database import db

def get_all_laboratories():
    return Laboratory.query.all()

def get_laboratory_by_id(lab_id):
    return Laboratory.query.get(lab_id)

def create_laboratory(name):
    lab = Laboratory(name=name)
    db.session.add(lab)
    db.session.commit()
    return lab

def update_laboratory(lab_id, name):
    lab = Laboratory.query.get(lab_id)
    if lab:
        lab.name = name
        db.session.commit()
    return lab

def delete_laboratory(lab_id):
    lab = Laboratory.query.get(lab_id)
    if lab:
        db.session.delete(lab)
        db.session.commit()
    return lab