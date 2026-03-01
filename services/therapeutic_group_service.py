from models.therapeutic_group import TherapeuticGroup
from database import db

def get_all_groups():
    return TherapeuticGroup.query.all()

def get_group_by_id(group_id):
    return TherapeuticGroup.query.get(group_id)

def create_group(data):
    group = TherapeuticGroup(**data)
    db.session.add(group)
    db.session.commit()
    return group

def update_group(group_id, data):
    group = TherapeuticGroup.query.get(group_id)
    if group:
        for key, value in data.items():
            setattr(group, key, value)
        db.session.commit()
    return group

def delete_group(group_id):
    group = TherapeuticGroup.query.get(group_id)
    if group:
        db.session.delete(group)
        db.session.commit()
    return group