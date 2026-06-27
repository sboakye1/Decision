from werkzeug.security import check_password_hash
from database.connection import get_db_connection
from datetime import datetime


class AuthService:
    @staticmethod
    def current_timestamp():
        return datetime.utcnow().isoformat()

    @staticmethod
    def authenticate_user(email: str, password: str):
        query = (
            "SELECT user_id, name, email, password_hash, role "
            "FROM users WHERE email = %s LIMIT 1"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if not user:
                return None

            if not check_password_hash(user["password_hash"], password):
                return None

            return user
        finally:
            cursor.close()
            conn.close()
