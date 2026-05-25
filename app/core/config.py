import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASS     = os.getenv("EMAIL_PASS")
MODEL_NAME     = "gemini-2.5-flash"
