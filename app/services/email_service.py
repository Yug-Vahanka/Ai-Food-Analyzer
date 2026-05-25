import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException
from app.core.config import EMAIL_USER, EMAIL_PASS
from app.services.calorie_service import extract_calories


def send_daily_summary(username: str, email: str, today: str, rows: list):
    """
    Send a daily nutrition summary email.
    rows : list of (query, meal_type, response) for today
    """
    if not EMAIL_USER or not EMAIL_PASS:
        raise HTTPException(
            status_code=500,
            detail="Email not configured. Set EMAIL_USER and EMAIL_PASS in .env",
        )

    if not rows:
        return {"msg": "No food logged today — email not sent"}

    total = 0
    lines = [f"Daily Food Summary for {username} — {today}\n"]
    for q, m, r in rows:
        cals   = extract_calories(r)
        total += cals
        lines.append(f"• [{m}] {q} — {cals} kcal")

    lines.append(f"\nTotal Calories Today: {total} kcal")
    body = "\n".join(lines)

    try:
        msg            = MIMEText(body)
        msg["Subject"] = f"Your Food Summary — {today}"
        msg["From"]    = EMAIL_USER
        msg["To"]      = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return {"msg": f"Summary sent to {email}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email failed: {str(e)}")
