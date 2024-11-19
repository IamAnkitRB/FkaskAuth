from db_connection import get_db_connection
from datetime import datetime, timedelta

class OTP:
    @staticmethod
    def create(user_id, otp):
        """Create a new OTP entry."""
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO otps (user_id, otp, created_at) VALUES (%s, %s, %s) RETURNING id;",
                    (user_id, otp, datetime.utcnow()),
                )
                return cursor.fetchone()["id"]

    @staticmethod
    def get_latest_by_user_id(user_id):
        """Fetch the latest OTP for a user."""
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM otps WHERE user_id = %s ORDER BY created_at DESC LIMIT 1;",
                    (user_id,),
                )
                return cursor.fetchone()

    @staticmethod
    def delete(otp_id):
        """Delete an OTP entry by ID."""
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM otps WHERE id = %s;", (otp_id,))
                conn.commit()        
