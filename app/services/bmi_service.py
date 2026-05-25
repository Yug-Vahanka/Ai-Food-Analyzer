def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    """
    Calculate BMI and return category + recommended daily calories.
    Formula: BMI = weight(kg) / height(m)^2
    """
    if height_cm <= 0 or weight_kg <= 0:
        return {"bmi": 0, "category": "Unknown", "recommended_calories": 2000}

    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)

    if bmi < 18.5:
        category    = "Underweight"
        recommended = 2500
    elif bmi < 25:
        category    = "Normal"
        recommended = 2000
    elif bmi < 30:
        category    = "Overweight"
        recommended = 1700
    else:
        category    = "Obese"
        recommended = 1500

    return {"bmi": bmi, "category": category, "recommended_calories": recommended}
