from google import genai
from PIL import Image
from app.core.config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)


def get_food_analysis(food: str) -> str:
    """Send a food name to Gemini and get a detailed nutrition breakdown."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"""
        Analyze the food: {food}

        IMPORTANT: Always write calories exactly like this → Calories: XX kcal

        Provide:
        - Calories (in kcal)
        - Protein (g)
        - Carbohydrates (g)
        - Fats (g)
        - Vitamins & Minerals (brief)
        - Health suggestion (1-2 lines)
        """,
    )
    return response.text


def analyze_image(image: Image.Image) -> str:
    """Send a PIL Image to Gemini for food identification and nutrition."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            "Identify this food and give a full nutrition breakdown. "
            "Always include 'Calories: XX kcal' in your response.",
            image,
        ],
    )
    return response.text
