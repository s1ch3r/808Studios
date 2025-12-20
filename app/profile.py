from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from app.models import User, Booking

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/profile")
def profile(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()

    user = db.query(User).get(request.session["user_id"])

    bookings = (
        db.query(Booking)
        .join(Booking.studio)
        .filter(Booking.user_id == user.id)
        .order_by(Booking.date, Booking.start_time)
        .all()
    )

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": user,
            "bookings": bookings
        }
    )
