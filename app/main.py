from fastapi import FastAPI
from app.db.database import init_db
from app.api import auth, food, analytics, profile, export

app = FastAPI(title="AI Food Analyzer")

# Initialise database tables on startup
init_db()

# Mount all route groups
app.include_router(auth.router)
app.include_router(food.router)
app.include_router(analytics.router)
app.include_router(profile.router)
app.include_router(export.router)
