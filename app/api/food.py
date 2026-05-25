import io
from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Depends
from PIL import Image
from app.core.security import get_current_user
from app.services.gemini_service import get_food_analysis, analyze_image
from app.db import models

router = APIRouter()


@router.post("/analyze")
def analyze(
    food: str      = Form(...),
    meal_type: str = Form(default="Other"),
    username: str  = Depends(get_current_user),
):
    """Analyze a food by name using Gemini and save to history."""
    result = get_food_analysis(food)
    models.insert_history(username, food, result, meal_type)
    return {"result": result}


@router.post("/image")
async def image(
    file: UploadFile = File(...),
    meal_type: str   = Form(default="Other"),
    username: str    = Depends(get_current_user),
):
    """Accept an uploaded food image, analyze it with Gemini Vision."""
    try:
        contents  = await file.read()
        img       = Image.open(io.BytesIO(contents))
        result    = analyze_image(img)
        first_line = result.strip().split("\n")[0][:60]
        food_label = f"📷 {first_line}" if first_line else "📷 Image"
        models.insert_history(username, food_label, result, meal_type)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")
