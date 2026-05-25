from fastapi import APIRouter, Form, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.core.security import (
    hash_password, verify_password, create_token,
    get_current_user, security,
)
from app.db import models
import sqlite3

router = APIRouter()


@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    """Create a new user account with a bcrypt-hashed password."""
    try:
        models.create_user(username, hash_password(password))
        return {"msg": "Registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    """Verify credentials and return a secure session token."""
    row = models.get_user(username)
    if not row or not verify_password(password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token()
    models.save_session(token, username)
    return {"msg": "success", "token": token}


@router.post("/logout")
def logout(
    username: str = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Invalidate the current session token."""
    models.delete_session(credentials.credentials)
    return {"msg": "Logged out"}
