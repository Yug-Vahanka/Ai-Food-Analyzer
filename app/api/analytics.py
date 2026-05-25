from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db import models
from app.services.calorie_service import extract_calories
from app.utils.helpers import last_n_dates

router = APIRouter()


@router.get("/analytics")
def analytics(username: str = Depends(get_current_user)):
    """Return full food history with extracted calorie count per entry."""
    rows = models.get_history(username)
    data = [
        {
            "query":     q,
            "response":  r,
            "meal_type": m,
            "date":      d,
            "calories":  extract_calories(r),
        }
        for q, r, m, d in rows
    ]
    return {"total_queries": len(data), "history": data}


@router.get("/weekly")
def weekly(username: str = Depends(get_current_user)):
    """Return total calories per day for the last 7 days."""
    dates = last_n_dates(7)
    rows  = models.get_history_since(username, dates[0])

    daily = {d: 0 for d in dates}
    for logged_date, response in rows:
        if logged_date in daily:
            daily[logged_date] += extract_calories(response)

    return {"weekly": [{"date": d, "calories": daily[d]} for d in dates]}


@router.get("/my_data")
def my_data(username: str = Depends(get_current_user)):
    """Return all raw history rows for the logged-in user."""
    rows = models.get_history_full(username)
    data = [
        {"id": r[0], "username": r[1], "query": r[2],
         "response": r[3], "meal_type": r[4], "date": r[5]}
        for r in rows
    ]
    return {"data": data}


@router.delete("/delete_history")
def delete_history(username: str = Depends(get_current_user)):
    """Permanently delete all food history for the logged-in user."""
    models.delete_history(username)
    return {"msg": "History deleted"}
