from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from passlib.hash import bcrypt
from app.database import SessionLocal
from app.models import User

router = APIRouter()


@router.post("/register")
def register(email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return {"error": "User already exists"}

        user = User(email=email, password=bcrypt.hash(password))
        db.add(user)
        db.commit()
    finally:
        db.close()

    return RedirectResponse("/", status_code=302)


@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user and bcrypt.verify(password, user.password):
            request.session["user_id"] = user.id
            request.session["is_admin"] = user.is_admin
    finally:
        db.close()

    return RedirectResponse("/", status_code=302)
