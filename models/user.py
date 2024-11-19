from db_connection import get_db_connection
from datetime import datetime

class User:
    @staticmethod
    def create(email):
        """Create a new user."""
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (email, created_at) VALUES (%s, %s) RETURNING id;",
                    (email, datetime.utcnow()),
                )
                return cursor.fetchone()["id"]

    @staticmethod
    def get_by_email(email):
        """Fetch a user by email."""
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
                return cursor.fetchone()
