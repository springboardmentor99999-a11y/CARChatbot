# backend/auth/service.py

from auth.models import create_user, get_user_by_email
from auth.security import hash_password, verify_password, create_access_token

def register_user(name, email, password):
    pwd_hash = hash_password(password.strip())
    create_user(name.strip(), email.strip().lower(), pwd_hash)


def authenticate_user(email, password):
    user = get_user_by_email(email.strip().lower())

    if not user:
        return None

    uid, name, email, pwd_hash = user

    if not verify_password(password.strip(), pwd_hash):
        return None

    token = create_access_token({
        "sub": email,
        "name": name
    })

    return token


def reset_password(email, new_password):
    from database import get_connection
    from auth.security import hash_password

    email = email.strip().lower()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password_hash=? WHERE email=?",
        (hash_password(new_password.strip()), email),
    )

    conn.commit()
    updated = cur.rowcount

    conn.close()

    return updated > 0

