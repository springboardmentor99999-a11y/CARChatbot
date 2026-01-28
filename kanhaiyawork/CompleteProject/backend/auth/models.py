# backend/auth/models.py

from database import get_connection

def create_user(name, email, pwd_hash):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (full_name,email,password_hash) VALUES (?,?,?)",
        (name, email, pwd_hash),
    )

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, full_name, email, password_hash FROM users WHERE email=?",
        (email,),
    )

    row = cur.fetchone()
    conn.close()

    return row
