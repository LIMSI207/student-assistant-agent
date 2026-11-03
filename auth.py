import sqlite3
import hashlib
import secrets
import hmac
import re

from database import DB_NAME


def init_auth_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        200000
    ).hex()

    return password_hash, salt


def register_user(name, email, password):
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "All fields are required."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Enter a valid email address."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    password_hash, salt = hash_password(password)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                """INSERT INTO users
                   (name, email, password_hash, salt)
                   VALUES (?, ?, ?, ?)""",
                (name, email, password_hash, salt)
            )

        return True, "Registration successful!"

    except sqlite3.IntegrityError:
        return False, "This email is already registered."


def login_user(email, password):
    email = email.strip().lower()

    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

    if user is None:
        return None

    password_hash, _ = hash_password(
        password, user["salt"]
    )

    if hmac.compare_digest(
        password_hash, user["password_hash"]
    ):
        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }

    return None