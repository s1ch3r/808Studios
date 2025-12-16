from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine
from app import models
from app.auth import router as auth_router
from app.booking import router as booking_router
from app.admin import router as admin_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret")

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_router)
app.include_router(booking_router)
app.include_router(admin_router)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
