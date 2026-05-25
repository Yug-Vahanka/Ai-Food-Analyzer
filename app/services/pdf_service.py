import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib import colors
from app.services.calorie_service import extract_calories
from app.services.bmi_service import calculate_bmi


def generate_pdf(username: str, rows: list, profile_row) -> io.BytesIO:
    """
    Build a PDF report in memory and return the BytesIO buffer.
    rows    : list of (query, meal_type, logged_date, response)
    profile_row : raw DB row for the user's profile
    """
    buffer = io.BytesIO()
    c = pdf_canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkgreen)
    c.drawString(50, height - 50, f"Food Report — {username}")

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(50, height - 70, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    y = height - 100

    # Profile summary
    if profile_row:
        keys = ["username", "height_cm", "weight_kg", "age", "gender", "activity", "calorie_goal"]
        p    = dict(zip(keys, profile_row))
        bmi  = calculate_bmi(p["weight_kg"], p["height_cm"])

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Profile Summary")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(
            50, y,
            f"Height: {p['height_cm']} cm   Weight: {p['weight_kg']} kg   "
            f"BMI: {bmi['bmi']} ({bmi['category']})   "
            f"Daily Goal: {p['calorie_goal']} kcal",
        )
        y -= 30

    # Food history
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Food History")
    y -= 20

    total_calories = 0
    for q, m, d, r in rows:
        cals            = extract_calories(r)
        total_calories += cals

        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{d}  [{m}]  {q[:60]}  —  {cals} kcal")
        y -= 15

        for line in r.strip().split("\n")[:2]:
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.grey)
            c.drawString(60, y, line[:100])
            c.setFillColor(colors.black)
            y -= 13

        y -= 5

        if y < 80:
            c.showPage()
            y = height - 50

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.darkgreen)
    c.drawString(50, y - 10, f"Total Calories Logged: {total_calories} kcal")

    c.save()
    buffer.seek(0)
    return buffer
