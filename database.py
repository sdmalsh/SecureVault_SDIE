import sqlite3
import hashlib
import os
import re

# =========================
# Database Path
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

# =========================
# Password Hashing
# =========================

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def is_hashed_password(password):
    """Return True if the stored password looks like a SHA-256 hash."""
    return bool(re.fullmatch(r"[0-9a-f]{64}", password))

# =========================
# Create Database
# =========================

def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT

        )

    """)

    # Check if admin user already exists
    cursor.execute("SELECT id, password FROM users WHERE username = ?", ("admin",))
    admin_row = cursor.fetchone()

    if admin_row is None:
        # Add default admin user only if it doesn't exist
        hashed_password = hash_password("admin123")
        
        cursor.execute("""

            INSERT INTO users
            (username, password)

            VALUES (?, ?)

        """, ("admin", hashed_password))

    else:
        admin_id, existing_password = admin_row
        if not is_hashed_password(existing_password):
            # Migrate plain-text password to hashed password
            hashed_password = hash_password(existing_password)
            cursor.execute(
                "UPDATE users SET password = ? WHERE id = ?",
                (hashed_password, admin_id)
            )

    conn.commit()

    conn.close()

# =========================
# Check Login
# =========================

def check_login(username, password):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""

        SELECT * FROM users

        WHERE username = ?
        AND password = ?

    """, (username, hashed_password))

    user = cursor.fetchone()

    conn.close()

    return user

# =========================
# Add New User
# =========================

def add_user(username, password):
    """Add new user to database"""
    try:
        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        hashed_password = hash_password(password)

        cursor.execute("""

            INSERT INTO users
            (username, password)

            VALUES (?, ?)

        """, (username, hashed_password))

        conn.commit()

        conn.close()
        
        return True
    
    except sqlite3.IntegrityError:
        # Username already exists
        return False
    
    except Exception as e:
        print(f"Error adding user: {str(e)}")
        return False