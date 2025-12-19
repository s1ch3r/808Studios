from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt

from app.database import SessionLocal
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if password != user.password:
            # вариант мб попроще
            # raise HTTPException(status_code=400, detail="Неверный пароль")
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "error": "Неверный email или пароль"
                }
            )

        request.session["user_id"] = user.id
        request.session["is_admin"] = user.is_admin

        return RedirectResponse("/", status_code=302)
    finally:
        db.close()


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == email).first():
            return templates.TemplateResponse(
                "register.html",
                {
                    "request": request,
                    "error": "Пользователь с таким email уже существует"
                }
            )

        user = User(
            name=name,
            email=email,
            password=password
        )
        db.add(user)
        db.commit()

        request.session["user_id"] = user.id
        request.session["is_admin"] = user.is_admin

        return RedirectResponse("/", status_code=302)
    finally:
        db.close()


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)
