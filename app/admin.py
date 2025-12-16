from fastapi import APIRouter, Request
from app.database import SessionLocal
from app.models import Booking

router = APIRouter()


@router.get("/admin")
def admin_panel(request: Request):
    if not request.session.get("is_admin"):
        return {"error": "Access denied"}

    db = SessionLocal()
    try:
        bookings = db.query(Booking).all()
        return {
            "bookings": [
                {
                    "id": b.id,
                    "user_id": b.user_id,
                    "studio_id": b.studio_id,
                    "date": str(b.date),
                    "start_time": str(b.start_time),
                    "end_time": str(b.end_time),
                }
                for b in bookings
            ]
        }
    finally:
        db.close()
