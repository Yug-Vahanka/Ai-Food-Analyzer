from fastapi import APIRouter, Form, Depends
from app.core.security import get_current_user
from app.db import models
from app.services.bmi_service import calculate_bmi

router = APIRouter()


@router.get("/profile")
def get_profile(username: str = Depends(get_current_user)):
    """Return the user's saved profile with live BMI calculation."""
    row = models.get_profile(username)
    if not row:
        return {}

    keys    = ["username", "height_cm", "weight_kg", "age", "gender", "activity", "calorie_goal"]
    profile = dict(zip(keys, row))
    profile.update(calculate_bmi(profile["weight_kg"], profile["height_cm"]))
    return profile


@router.post("/profile")
def update_profile(
    height_cm:    float = Form(...),
    weight_kg:    float = Form(...),
    age:          int   = Form(...),
    gender:       str   = Form(...),
    activity:     str   = Form(...),
    calorie_goal: int   = Form(...),
    username:     str   = Depends(get_current_user),
):
    """Save or update the user's profile and return calculated BMI."""
    models.upsert_profile(username, height_cm, weight_kg, age, gender, activity, calorie_goal)
    bmi_data = calculate_bmi(weight_kg, height_cm)
    return {"msg": "Profile updated", **bmi_data, "calorie_goal": calorie_goal}
