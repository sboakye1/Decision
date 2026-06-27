from database.connection import get_db_connection


class AdminService:
    @staticmethod
    def get_latest_student_surveys(risk_filter=None):
        query = (
            "SELECT u.name AS student_name, s.program, s.level, ss.total_score, ss.risk_level, "
            "ss.recommendation, ss.survey_month "
            "FROM survey_summary ss "
            "JOIN (SELECT student_id, MAX(survey_month) AS latest_month "
            "FROM survey_summary GROUP BY student_id) latest "
            "ON ss.student_id = latest.student_id AND ss.survey_month = latest.latest_month "
            "JOIN students s ON ss.student_id = s.student_id "
            "JOIN users u ON s.user_id = u.user_id "
        "")
        params = []

        if risk_filter in ("Low", "Medium", "High"):
            query += "WHERE ss.risk_level = %s "
            params.append(risk_filter)

        query += (
            "ORDER BY FIELD(ss.risk_level, 'High', 'Medium', 'Low'), ss.survey_month DESC"
        )

        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
