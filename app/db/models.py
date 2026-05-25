from app.db.database import get_cursor


def get_user(username: str):
    cursor, _ = get_cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    return cursor.fetchone()


def create_user(username: str, hashed_password: str):
    cursor, conn = get_cursor()
    cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, hashed_password))
    cursor.execute("INSERT OR IGNORE INTO profiles (username) VALUES (?)", (username,))
    conn.commit()


def save_session(token: str, username: str):
    cursor, conn = get_cursor()
    cursor.execute("INSERT INTO sessions VALUES (?, ?)", (token, username))
    conn.commit()


def delete_session(token: str):
    cursor, conn = get_cursor()
    cursor.execute("DELETE FROM sessions WHERE token=?", (token,))
    conn.commit()


def insert_history(username: str, query: str, response: str, meal_type: str):
    cursor, conn = get_cursor()
    cursor.execute(
        "INSERT INTO history (username, query, response, meal_type) VALUES (?, ?, ?, ?)",
        (username, query, response, meal_type),
    )
    conn.commit()


def get_history(username: str):
    cursor, _ = get_cursor()
    cursor.execute(
        "SELECT query, response, meal_type, logged_date FROM history WHERE username=?",
        (username,),
    )
    return cursor.fetchall()


def get_history_full(username: str):
    cursor, _ = get_cursor()
    cursor.execute("SELECT * FROM history WHERE username=?", (username,))
    return cursor.fetchall()


def get_history_today(username: str, today: str):
    cursor, _ = get_cursor()
    cursor.execute(
        "SELECT query, meal_type, response FROM history WHERE username=? AND logged_date=?",
        (username, today),
    )
    return cursor.fetchall()


def get_history_since(username: str, since: str):
    cursor, _ = get_cursor()
    cursor.execute(
        "SELECT logged_date, response FROM history WHERE username=? AND logged_date >= ?",
        (username, since),
    )
    return cursor.fetchall()


def delete_history(username: str):
    cursor, conn = get_cursor()
    cursor.execute("DELETE FROM history WHERE username=?", (username,))
    conn.commit()


def get_profile(username: str):
    cursor, _ = get_cursor()
    cursor.execute("SELECT * FROM profiles WHERE username=?", (username,))
    return cursor.fetchone()


def upsert_profile(username, height_cm, weight_kg, age, gender, activity, calorie_goal):
    cursor, conn = get_cursor()
    cursor.execute(
        """
        INSERT INTO profiles (username, height_cm, weight_kg, age, gender, activity, calorie_goal)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            height_cm=excluded.height_cm,
            weight_kg=excluded.weight_kg,
            age=excluded.age,
            gender=excluded.gender,
            activity=excluded.activity,
            calorie_goal=excluded.calorie_goal
        """,
        (username, height_cm, weight_kg, age, gender, activity, calorie_goal),
    )
    conn.commit()
