import bcrypt
import secrets
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.database import get_cursor

security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt with auto salt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Check a plain-text password against a stored bcrypt hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_token() -> str:
    """Generate a cryptographically secure session token (64 hex chars)."""
    return secrets.token_hex(32)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Validate the Bearer token and return the username, or raise 401."""
    cursor, conn = get_cursor()
    token = credentials.credentials
    cursor.execute("SELECT username FROM sessions WHERE token=?", (token,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return row[0]
