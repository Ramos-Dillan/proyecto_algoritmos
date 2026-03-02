from sqlalchemy.orm import Session
from models.user import User
from auth.auth_handler import hash_password, verify_password

def register_user(db: Session, username: str, password: str):
    existing_user = db.query(User).filter(User.username == username).first()
    
    if existing_user:
        return None
    
    hashed = hash_password(password)
    user = User(username=username, password=hashed)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.password):
        return None
    
    return user