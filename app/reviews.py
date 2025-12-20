from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from app.models import Review

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/studios/{studio_id}/reviews")
def add_review(
    request: Request,
    studio_id: int,
    text: str = Form(...)
):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()

    review = Review(
        text=text,
        user_id=request.session["user_id"],
        studio_id=studio_id
    )

    db.add(review)
    db.commit()

    return RedirectResponse(f"/studios/{studio_id}", status_code=302)


@router.get("/reviews/{review_id}/edit")
def edit_review_page(request: Request, review_id: int):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()
    review = db.query(Review).get(review_id)

    if not review or review.user_id != request.session["user_id"]:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "edit_review.html",
        {"request": request, "review": review}
    )


@router.post("/reviews/{review_id}/edit")
def edit_review(
    request: Request,
    review_id: int,
    text: str = Form(...)
):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()
    review = db.query(Review).get(review_id)

    if not review or review.user_id != request.session["user_id"]:
        return RedirectResponse("/", status_code=302)

    review.text = text
    db.commit()

    return RedirectResponse(f"/studios/{review.studio_id}", status_code=302)


@router.post("/reviews/{review_id}/delete")
def delete_review(request: Request, review_id: int):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    db = SessionLocal()
    review = db.query(Review).get(review_id)

    if not review or review.user_id != request.session["user_id"]:
        return RedirectResponse("/", status_code=302)

    studio_id = review.studio_id
    db.delete(review)
    db.commit()

    return RedirectResponse(f"/studios/{studio_id}", status_code=302)
