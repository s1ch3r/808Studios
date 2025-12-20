from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from datetime import datetime, timedelta, date as date_cls

from app.database import SessionLocal
from app.models import Studio, Booking

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def error_response(message: str, studio: Studio, request: Request):
    return templates.TemplateResponse(
        "book_studio.html",
        {
            "request": request,
            "studio": studio,
            "error": message,
            "busy_hours": set(),
            "date": date_cls.today()
        },
        status_code=400
    )


@router.get("/studios")
def list_studios(request: Request):
    db = SessionLocal()
    studios = db.query(Studio).filter(Studio.is_active == True).all()

    return templates.TemplateResponse(
        "studios.html",
        {"request": request, "studios": studios}
    )


@router.get("/studios/{studio_id}/book")
def book_page(
    request: Request,
    studio_id: int,
    date: str | None = None
):
    db = SessionLocal()
    studio = db.query(Studio).get(studio_id)

    if not studio:
        return RedirectResponse("/studios", status_code=302)

    booking_date = (
        datetime.strptime(date, "%Y-%m-%d").date()
        if date else date_cls.today()
    )

    bookings = db.query(Booking).filter(
        Booking.studio_id == studio_id,
        Booking.date == booking_date
    ).all()

    busy_hours = set()

    for b in bookings:
        current = datetime.combine(booking_date, b.start_time)
        end = datetime.combine(booking_date, b.end_time)

        while current < end:
            busy_hours.add(current.time().strftime("%H:%M"))
            current += timedelta(hours=1)

    return templates.TemplateResponse(
        "book_studio.html",
        {
            "request": request,
            "studio": studio,
            "busy_hours": busy_hours,
            "date": booking_date
        }
    )


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
    studio = db.query(Studio).get(studio_id)

    if not studio:
        return RedirectResponse("/studios", status_code=302)

    booking_date = datetime.strptime(date, "%Y-%m-%d").date()
    start = datetime.strptime(start_time, "%H:%M")
    end = start + timedelta(hours=hours)

    now = datetime.now()

    if booking_date < date_cls.today():
        return error_response("Нельзя бронировать в прошлом", studio, request)
    if booking_date == date_cls.today() and start.time() <= now.time():
        return error_response("Нельзя бронировать прошедшее время", studio, request)

    if start.time() < studio.work_start:
        return error_response("Студия ещё закрыта", studio, request)
    if end.time() > studio.work_end:
        return error_response("Студия уже закрыта", studio, request)

    booking = Booking(
        user_id=request.session["user_id"],
        studio_id=studio_id,
        date=booking_date,
        start_time=start.time(),
        end_time=end.time()
    )

    db.add(booking)
    db.commit()

    return RedirectResponse("/profile", status_code=302)


@router.get("/studios/{studio_id}")
def studio_detail(request: Request, studio_id: int):
    db = SessionLocal()

    studio = db.query(Studio).get(studio_id)

    return templates.TemplateResponse(
        "studio_detail.html",
        {
            "request": request,
            "studio": studio,
            "reviews": studio.reviews
        }
    )
