from database.connection import get_db_connection


class StudentService:
    @staticmethod
    def get_profile(user_id):
        query = (
            "SELECT s.student_id, u.name, u.email, s.program, s.level "
            "FROM students s "
            "JOIN users u ON s.user_id = u.user_id "
            "WHERE u.user_id = %s LIMIT 1"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_latest_survey(student_id):
        query = (
            "SELECT survey_month, total_score, stress_level, risk_level, recommendation "
            "FROM survey_summary "
            "WHERE student_id = %s "
            "ORDER BY survey_month DESC "
            "LIMIT 1"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (student_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
