from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Booking

router = APIRouter()


@router.post("/book")
def book(
    request: Request,
    studio_id: int = Form(...),
    date: str = Form(...),
    start_time: str = Form(...),
    hours: int = Form(...)
):
    if "user_id" not in request.session:
        return {"error": "Not authenticated"}

    db = SessionLocal()
    try:
        booking_date = datetime.strptime(date, "%Y-%m-%d").date()
        start = datetime.strptime(start_time, "%H:%M").time()
        end = (datetime.strptime(start_time, "%H:%M") + timedelta(hours=hours)).time()

        booking = Booking(
            user_id=request.session["user_id"],
            studio_id=studio_id,
            date=booking_date,
            start_time=start,
            end_time=end
        )

        db.add(booking)
        db.commit()
    finally:
        db.close()

    return RedirectResponse("/", status_code=302)
