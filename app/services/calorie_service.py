import re


def extract_calories(text: str) -> int:
    """
    Parse calorie count from Gemini's response text.
    Looks for patterns like 'Calories: 350 kcal' or '350 cal'.
    Returns 0 if no calorie info is found.
    """
    text_lower = text.lower()

    match = re.search(r"(\d+)\s*(kcal|cal)", text_lower)
    if match:
        return int(match.group(1))

    match2 = re.search(r"calories[:\s]+(\d+)", text_lower)
    if match2:
        return int(match2.group(1))

    return 0
