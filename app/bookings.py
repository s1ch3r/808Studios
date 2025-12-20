from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.database import SessionLocal
from app.models import Booking

router = APIRouter()


@router.post("/bookings/{booking_id}/cancel")
def cancel_booking(request: Request, booking_id: int):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()

    booking = db.query(Booking).get(booking_id)

    if not booking:
        return {"error": "Бронирование не найдено"}

    # может отменить сам или админ
    if (
        booking.user_id != request.session["user_id"]
        and not request.session.get("is_admin")
    ):
        return {"error": "Нет доступа"}

    db.delete(booking)
    db.commit()

    return RedirectResponse("/profile", status_code=302)
