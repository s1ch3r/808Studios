from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import Studio, Booking

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/studios")
def list_studios(request: Request):
    db = SessionLocal()
    try:
        studios = db.query(Studio).filter(Studio.is_active == True).all()
        return templates.TemplateResponse(
            "studios.html",
            {"request": request, "studios": studios}
        )
    finally:
        db.close()


@router.get("/studios/{studio_id}/book")
def book_page(request: Request, studio_id: int):
    db = SessionLocal()
    try:
        studio = db.get(Studio, studio_id)
        return templates.TemplateResponse(
            "book_studio.html",
            {"request": request, "studio": studio}
        )
    finally:
        db.close()


@router.post("/studios/{studio_id}/book")
def create_booking(
    request: Request,
    studio_id: int,
    date: str = Form(...),
    start_time: str = Form(...),
    hours: int = Form(...)
):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()
    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = start + timedelta(hours=hours)
        booking_date = datetime.strptime(date, "%Y-%m-%d").date()

        booking = Booking(
            user_id=request.session["user_id"],
            studio_id=studio_id,
            date=booking_date,
            start_time=start.time(),
            end_time=end.time()
        )

        db.add(booking)
        db.commit()
    finally:
        db.close()

    return RedirectResponse("/profile", status_code=302)
