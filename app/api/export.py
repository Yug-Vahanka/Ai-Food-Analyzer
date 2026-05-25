from datetime import datetime
from fastapi import APIRouter, Form, Depends
from fastapi.responses import StreamingResponse
from app.core.security import get_current_user
from app.db import models
from app.services.pdf_service import generate_pdf
from app.services.email_service import send_daily_summary

router = APIRouter()


@router.get("/export_pdf")
def export_pdf(username: str = Depends(get_current_user)):
    """Generate a PDF report of the user's food history."""
    rows        = models.get_history_full(username)
    # reorder columns to (query, meal_type, logged_date, response)
    pdf_rows    = [(r[2], r[4], r[5], r[3]) for r in rows]
    profile_row = models.get_profile(username)
    buffer      = generate_pdf(username, pdf_rows, profile_row)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={username}_food_report.pdf"},
    )


@router.post("/send_email")
def send_email(
    email: str    = Form(...),
    username: str = Depends(get_current_user),
):
    """Send a daily nutrition summary email."""
    today = datetime.now().date().isoformat()
    rows  = models.get_history_today(username, today)
    return send_daily_summary(username, email, today, rows)
