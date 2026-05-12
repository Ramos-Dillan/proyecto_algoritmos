from typing import Any, Tuple, Dict, Optional
from contextlib import contextmanager
from datetime import datetime, timedelta
import secrets
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from db.db import Sessionlocal
from db.models import User, Role
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import joinedload


@contextmanager
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def _send_reset_email(to_email: str, reset_link: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)
    frontend_name = os.getenv("APP_NAME", "Vademecum")

    subject = f"{frontend_name} - Restablecer contraseña"

    html = f"""
    <div style="font-family: Arial, sans-serif; line-height:1.5">
      <h2>Restablecer contraseña</h2>
      <p>Recibimos una solicitud para restablecer tu contraseña.</p>
      <p>
        <a href="{reset_link}" target="_blank"
           style="display:inline-block;padding:12px 18px;background:#2563eb;color:#fff;text-decoration:none;border-radius:8px;">
          Crear nueva contraseña
        </a>
      </p>
      <p>Este enlace expira en 1 hora.</p>
      <p>Si no pediste este cambio, ignora este correo.</p>
    </div>
    """

    if not smtp_host or not smtp_user or not smtp_pass:
        print(f"[DEV] Password reset link for {to_email}: {reset_link}")
        return True

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_from
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    return True


# =========================
# REGISTER
# =========================
def create_user(data: Dict[str, Any]) -> Tuple[Optional[dict], Any]:
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    identification = (data.get("identification") or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not email or not identification or not password:
        return None, {"message": "Todos los campos son requeridos"}

    with get_db() as db:
        if db.query(User).filter(User.username == username).first():
            return None, {"message": "El username ya existe"}

        if db.query(User).filter(User.email == email).first():
            return None, {"message": "El correo ya existe"}

        if db.query(User).filter(User.identification == identification).first():
            return None, {"message": "La identificación ya existe"}

        if email.endswith("@admin.com"):
            role_name = "admin"
        elif email.endswith("@medico.com"):
            role_name = "medico"
        else:
            role_name = "estudiante"

        role = db.query(Role).filter(Role.name == role_name).first()

        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.commit()
            db.refresh(role)

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            identification=identification,
            password=hashed_password,
            role_id=role.id
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "identification": user.identification,
            "role": role.name
        }, None


# =========================
# LOGIN
# =========================
def login_user(data: Dict[str, Any]) -> Tuple[Optional[dict], Any]:
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return None, {"message": "Email y password requeridos"}

    with get_db() as db:
        user = (
            db.query(User)
            .options(joinedload(User.role))
            .filter(User.email == email)
            .first()
        )

        if not user:
            return None, {"message": "Usuario no encontrado"}

        if user.is_active is False:
            return None, {"message": "Usuario desactivado"}

        if not check_password_hash(user.password, password):
            return None, {"message": "Password incorrecto"}

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "identification": user.identification,
            "role": user.role.name if user.role else None
        }, None


# =========================
# GET USERS
# =========================
def get_all_users():
    try:
        with get_db() as db:
            users = (
                db.query(User)
                .options(joinedload(User.role))
                .order_by(User.id.asc())
                .all()
            )

            data = []
            for u in users:
                data.append({
                    "id": u.id,
                    "username": u.username,
                    "email": u.email,
                    "identification": u.identification,
                    "role": u.role.name if u.role else None,
                    "is_active": u.is_active
                })

            return data, None

    except Exception as e:
        return None, {"message": str(e)}


# =========================
# UPDATE USER
# =========================
def update_user(user_id: int, data: Dict[str, Any]):
    try:
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, {"message": "Usuario no encontrado"}

            if "username" in data:
                user.username = data["username"]

            if "email" in data:
                user.email = data["email"]

            if "identification" in data:
                user.identification = data["identification"]

            if "is_active" in data:
                user.is_active = data["is_active"]

            db.commit()
            db.refresh(user)

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "identification": user.identification,
                "is_active": user.is_active
            }, None

    except Exception as e:
        return None, {"message": str(e)}


# =========================
# DELETE USER
# =========================
def delete_user(user_id: int):
    try:
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, {"message": "Usuario no encontrado"}

            db.delete(user)
            db.commit()

            return {"message": "Usuario eliminado correctamente"}, None

    except Exception as e:
        return None, {"message": str(e)}


# =========================
# FORGOT PASSWORD
# =========================
def forgot_password(data: Dict[str, Any]) -> Tuple[Optional[dict], Any]:
    email = (data.get("email") or "").strip().lower()

    if not email:
        return None, {"message": "Email requerido"}

    with get_db() as db:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return {"message": "Si el correo existe, recibirás instrucciones"}, None

        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)

        user.reset_token = token
        user.reset_token_expires = expires_at
        db.commit()

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:4200")
        reset_link = f"{frontend_url}/reset-password?token={token}"

        _send_reset_email(email, reset_link)

        return {"message": "Si el correo existe, recibirás instrucciones"}, None


# =========================
# RESET PASSWORD
# =========================
def reset_password(data: Dict[str, Any]) -> Tuple[Optional[dict], Any]:
    token = (data.get("token") or "").strip()
    new_password = (data.get("password") or "").strip()

    if not token or not new_password:
        return None, {"message": "Token y nueva contraseña son requeridos"}

    with get_db() as db:
        user = db.query(User).filter(User.reset_token == token).first()

        if not user:
            return None, {"message": "Token inválido"}

        if not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
            return None, {"message": "Token expirado"}

        user.password = generate_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()

        return {"message": "Contraseña actualizada correctamente"}, None