import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/food_ai.db")

conn   = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


def get_cursor():
    """Return (cursor, conn) for use in services and routes."""
    return cursor, conn


def init_db():
    """Create all tables if they don't exist yet."""

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT,
        query       TEXT,
        response    TEXT,
        meal_type   TEXT DEFAULT 'Other',
        logged_date TEXT DEFAULT (date('now'))
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token    TEXT PRIMARY KEY,
        username TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        username      TEXT PRIMARY KEY,
        height_cm     REAL    DEFAULT 0,
        weight_kg     REAL    DEFAULT 0,
        age           INTEGER DEFAULT 0,
        gender        TEXT    DEFAULT 'Other',
        activity      TEXT    DEFAULT 'Sedentary',
        calorie_goal  INTEGER DEFAULT 2000
    )
    """)

    conn.commit()
