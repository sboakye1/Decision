from datetime import datetime
from database.connection import get_db_connection


class CounselorService:
    @staticmethod
    def get_counselor_id(user_id):
        query = "SELECT counselor_id FROM counselors WHERE user_id = %s LIMIT 1"
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            counselor = cursor.fetchone()
            return counselor["counselor_id"] if counselor else None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def is_student_assigned(student_id, counselor_id):
        query = (
            "SELECT 1 FROM counselor_assignments "
            "WHERE student_id = %s AND counselor_id = %s AND status = 'active' LIMIT 1"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (student_id, counselor_id))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_assigned_students(counselor_id):
        query = (
            "SELECT u.name AS student_name, s.student_id, s.program, s.level, ss.total_score, ss.risk_level, "
            "ss.recommendation, ss.survey_month "
            "FROM counselor_assignments ca "
            "JOIN students s ON ca.student_id = s.student_id "
            "JOIN users u ON s.user_id = u.user_id "
            "JOIN survey_summary ss ON ss.student_id = s.student_id "
            "JOIN (SELECT student_id, MAX(survey_month) AS latest_month FROM survey_summary GROUP BY student_id) latest "
            "ON ss.student_id = latest.student_id AND ss.survey_month = latest.latest_month "
            "WHERE ca.counselor_id = %s AND ca.status = 'active' AND ss.risk_level IN ('High', 'Medium') "
            "ORDER BY FIELD(ss.risk_level, 'High', 'Medium'), ss.survey_month DESC"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (counselor_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_upcoming_appointments(counselor_id):
        query = (
            "SELECT a.appointment_id, a.student_id, a.appointment_date, a.status, u.name AS student_name "
            "FROM appointments a "
            "JOIN students s ON a.student_id = s.student_id "
            "JOIN users u ON s.user_id = u.user_id "
            "WHERE a.counselor_id = %s AND a.status = 'Pending' "
            "ORDER BY a.appointment_date ASC "
            "LIMIT 5"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (counselor_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_student_case_history(student_id, counselor_id):
        if not CounselorService.is_student_assigned(student_id, counselor_id):
            return None

        history_query = (
            "SELECT survey_month, total_score, stress_level, risk_level, recommendation "
            "FROM survey_summary "
            "WHERE student_id = %s "
            "ORDER BY survey_month DESC"
        )
        notes_query = (
            "SELECT note_id, note_text, created_at "
            "FROM counselor_notes "
            "WHERE student_id = %s AND counselor_id = %s "
            "ORDER BY created_at DESC"
        )
        profile_query = (
            "SELECT u.name AS student_name, s.program, s.level "
            "FROM students s "
            "JOIN users u ON s.user_id = u.user_id "
            "WHERE s.student_id = %s LIMIT 1"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(profile_query, (student_id,))
            profile = cursor.fetchone()

            cursor.execute(history_query, (student_id,))
            history = cursor.fetchall()

            cursor.execute(notes_query, (student_id, counselor_id))
            notes = cursor.fetchall()

            return {
                "profile": profile,
                "history": history,
                "notes": notes,
            }
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_note(student_id, counselor_id, note_text):
        if not CounselorService.is_student_assigned(student_id, counselor_id):
            return False

        query = (
            "INSERT INTO counselor_notes (student_id, counselor_id, note_text, created_at) "
            "VALUES (%s, %s, %s, NOW())"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (student_id, counselor_id, note_text))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def schedule_appointment(student_id, counselor_id, appointment_datetime, notes):
        if not CounselorService.is_student_assigned(student_id, counselor_id):
            return False

        query = (
            "INSERT INTO appointments (student_id, counselor_id, appointment_date, status, notes, created_at) "
            "VALUES (%s, %s, %s, 'Pending', %s, NOW())"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (student_id, counselor_id, appointment_datetime, notes))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()
