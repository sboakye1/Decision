from datetime import datetime
from database.connection import get_db_connection


class SurveyService:
    QUESTION_SET = [
        {"id": 1, "text": "I feel overwhelmed by academic pressure.", "category": "academic pressure"},
        {"id": 2, "text": "I have trouble falling asleep or staying asleep.", "category": "sleep"},
        {"id": 3, "text": "I feel anxious or nervous most days.", "category": "anxiety"},
        {"id": 4, "text": "I find it difficult to manage my stress.", "category": "stress"},
        {"id": 5, "text": "I feel socially isolated from my peers.", "category": "social well-being"},
        {"id": 6, "text": "I struggle to stay focused during classes.", "category": "academic pressure"},
        {"id": 7, "text": "I feel exhausted even after sleeping.", "category": "sleep"},
        {"id": 8, "text": "I worry about my future or performance frequently.", "category": "anxiety"},
        {"id": 9, "text": "I feel lonely or disconnected in social situations.", "category": "social well-being"},
        {"id": 10, "text": "I feel pressure from my coursework and deadlines.", "category": "academic pressure"},
    ]

    ANSWER_MAP = {
        "Never": 0,
        "Rarely": 1,
        "Sometimes": 2,
        "Often": 3,
        "Always": 4,
    }

    @classmethod
    def question_keys(cls):
        return [f"question_{q['id']}" for q in cls.QUESTION_SET]

    @classmethod
    def get_questions(cls):
        return cls.QUESTION_SET

    @classmethod
    def validate_answers(cls, answers):
        return all(answers.get(key) in cls.ANSWER_MAP for key in cls.question_keys())

    @classmethod
    def map_answer_score(cls, answer_value):
        return cls.ANSWER_MAP.get(answer_value, 0)

    @classmethod
    def current_month(cls):
        return datetime.utcnow().strftime("%Y-%m")

    @classmethod
    def get_student_id_for_user(cls, user_id):
        query = "SELECT student_id FROM students WHERE user_id = %s LIMIT 1"
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            student = cursor.fetchone()
            return student["student_id"] if student else None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def has_submitted_current_month(cls, student_id):
        query = (
            "SELECT 1 FROM survey_summary "
            "WHERE student_id = %s AND survey_month = %s LIMIT 1"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (student_id, cls.current_month()))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def calculate_risk_and_recommendation(cls, total_score):
        if total_score <= 10:
            return "Low", "Low", "No action needed"
        if total_score <= 20:
            return "Medium", "Medium", "Monitor student and suggest counseling"
        return "High", "High", "Immediate counseling required"

    @classmethod
    def process_submission(cls, student_id, answers):
        scores = [cls.map_answer_score(value) for value in answers.values()]
        total_score = sum(scores)
        stress_level, risk_level, recommendation = cls.calculate_risk_and_recommendation(total_score)
        survey_month = cls.current_month()

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            insert_summary = (
                "INSERT INTO survey_summary "
                "(student_id, survey_month, total_score, stress_level, risk_level, recommendation) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(
                insert_summary,
                (student_id, survey_month, total_score, stress_level, risk_level, recommendation),
            )
            conn.commit()

            for question_id, answer_value in enumerate(answers.values(), start=1):
                score = cls.map_answer_score(answer_value)
                insert_response = (
                    "INSERT INTO survey_responses "
                    "(student_id, question_id, answer_value, score, survey_month, submitted_at) "
                    "VALUES (%s, %s, %s, %s, %s, NOW())"
                )
                cursor.execute(
                    insert_response,
                    (student_id, question_id, answer_value, score, survey_month),
                )
            conn.commit()

            return {
                "student_id": student_id,
                "survey_month": survey_month,
                "total_score": total_score,
                "stress_level": stress_level,
                "risk_level": risk_level,
                "recommendation": recommendation,
            }
        finally:
            cursor.close()
            conn.close()
