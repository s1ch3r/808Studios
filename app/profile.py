from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from app.models import Booking, Studio

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/profile")
def profile(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()
    try:
        bookings = (
            db.query(Booking)
            .join(Studio)
            .filter(Booking.user_id == request.session["user_id"])
            .order_by(Booking.date, Booking.start_time)
            .all()
        )

        return templates.TemplateResponse(
            "profile.html",
            {
                "request": request,
                "bookings": bookings
            }
        )
    finally:
        db.close()
