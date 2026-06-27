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
        )
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

    @staticmethod
    def get_assignable_students(risk_filter=None):
        query = (
            "SELECT u.name AS student_name, s.student_id, s.program, s.level, ss.total_score, ss.risk_level, "
            "ss.recommendation, ss.survey_month, ca.assignment_id, ca.counselor_id, cu.name AS counselor_name "
            "FROM survey_summary ss "
            "JOIN (SELECT student_id, MAX(survey_month) AS latest_month FROM survey_summary GROUP BY student_id) latest "
            "ON ss.student_id = latest.student_id AND ss.survey_month = latest.latest_month "
            "JOIN students s ON ss.student_id = s.student_id "
            "JOIN users u ON s.user_id = u.user_id "
            "LEFT JOIN counselor_assignments ca ON ca.student_id = s.student_id AND ca.status = 'active' "
            "LEFT JOIN counselors c ON ca.counselor_id = c.counselor_id "
            "LEFT JOIN users cu ON c.user_id = cu.user_id "
            "WHERE ss.risk_level IN ('High', 'Medium') "
        )
        params = []

        if risk_filter in ('High', 'Medium'):
            query += "AND ss.risk_level = %s "
            params.append(risk_filter)

        query += (
            "ORDER BY FIELD(ss.risk_level, 'High', 'Medium'), ss.survey_month DESC"
        )

        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_counselor_workload():
        query = (
            "SELECT c.counselor_id, u.name AS counselor_name, "
            "COUNT(ca.assignment_id) AS assigned_count "
            "FROM counselors c "
            "JOIN users u ON c.user_id = u.user_id "
            "LEFT JOIN counselor_assignments ca ON ca.counselor_id = c.counselor_id AND ca.status = 'active' "
            "GROUP BY c.counselor_id"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            counselors = cursor.fetchall()
            for counselor in counselors:
                count = counselor["assigned_count"]
                if count >= 15:
                    counselor["status"] = "Overloaded"
                elif count >= 10:
                    counselor["status"] = "Busy"
                else:
                    counselor["status"] = "Available"
            return counselors
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_active_assignment(student_id):
        query = (
            "SELECT assignment_id, counselor_id FROM counselor_assignments "
            "WHERE student_id = %s AND status = 'active' LIMIT 1"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (student_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_analytics_data():
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            # Snapshot: latest survey per student
            latest_q = (
                "SELECT ss.student_id, ss.total_score, ss.risk_level "
                "FROM survey_summary ss "
                "JOIN (SELECT student_id, MAX(survey_month) AS latest_month FROM survey_summary GROUP BY student_id) latest "
                "ON ss.student_id = latest.student_id AND ss.survey_month = latest.latest_month"
            )
            cursor.execute(latest_q)
            latest_rows = cursor.fetchall()
            total_students = len(latest_rows)
            risk_counts = {"High": 0, "Medium": 0, "Low": 0}
            total_score = 0
            for r in latest_rows:
                rl = r.get("risk_level")
                if rl in risk_counts:
                    risk_counts[rl] += 1
                total_score += r.get("total_score", 0)
            avg_score = round(total_score / total_students, 2) if total_students else 0.0

            # Monthly trend: average score per month (uses survey_summary history)
            cursor.execute(
                "SELECT survey_month, AVG(total_score) AS avg_score "
                "FROM survey_summary GROUP BY survey_month ORDER BY survey_month ASC"
            )
            trend_rows = cursor.fetchall()
            monthly_trend = [{"month": tr["survey_month"], "avg_score": float(tr["avg_score"])} for tr in trend_rows]

            # Assigned students and pending appointments
            cursor.execute("SELECT COUNT(DISTINCT student_id) AS assigned_count FROM counselor_assignments WHERE status = 'active'")
            assigned_count = cursor.fetchone().get("assigned_count", 0)

            cursor.execute("SELECT COUNT(*) AS pending_count FROM appointments WHERE status = 'Pending'")
            pending_count = cursor.fetchone().get("pending_count", 0)

            # Insights: compare last two months high risk counts
            cursor.execute(
                """SELECT survey_month, SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) AS high_count
                FROM survey_summary
                GROUP BY survey_month
                ORDER BY survey_month DESC
                LIMIT 2"""
            )
            last_two = cursor.fetchall()
            high_trend = None
            if len(last_two) >= 2:
                current = last_two[0]["high_count"]
                previous = last_two[1]["high_count"]
                if current > previous:
                    high_trend = "increasing"
                elif current < previous:
                    high_trend = "decreasing"
                else:
                    high_trend = "stable"
            insights = []
            if high_trend == "increasing":
                insights.append("High risk students are increasing this month.")
            elif high_trend == "decreasing":
                insights.append("High risk students are decreasing compared to last month.")
            else:
                insights.append("High risk student counts are stable.")

            # Majority risk level
            majority = max(risk_counts, key=lambda k: risk_counts[k]) if total_students else None
            if majority:
                insights.append(f"Most students fall under {majority.lower()} stress level.")

            # Counseling demand trend (pending appointments by month)
            cursor.execute(
                """SELECT DATE_FORMAT(appointment_date, '%%Y-%%m') AS m, COUNT(*) as cnt
                FROM appointments
                WHERE status = 'Pending'
                GROUP BY m
                ORDER BY m DESC
                LIMIT 2"""
            )
            appts = cursor.fetchall()
            if len(appts) >= 2 and appts[0]["cnt"] > appts[1]["cnt"]:
                insights.append("Counseling demand is rising.")
            elif len(appts) >= 2 and appts[0]["cnt"] < appts[1]["cnt"]:
                insights.append("Counseling demand is decreasing.")
            else:
                insights.append("Counseling demand is stable.")

            return {
                "total_students": total_students,
                "risk_counts": risk_counts,
                "avg_score": avg_score,
                "monthly_trend": monthly_trend,
                "assigned_count": assigned_count,
                "pending_count": pending_count,
                "insights": insights,
            }
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def assign_student(student_id, counselor_id):
        existing = AdminService.get_active_assignment(student_id)
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            if existing:
                cursor.execute(
                    "UPDATE counselor_assignments SET counselor_id = %s, assigned_date = CURDATE() "
                    "WHERE assignment_id = %s",
                    (counselor_id, existing["assignment_id"]),
                )
            else:
                cursor.execute(
                    "INSERT INTO counselor_assignments "
                    "(student_id, counselor_id, assigned_date, status) "
                    "VALUES (%s, %s, CURDATE(), 'active')",
                    (student_id, counselor_id),
                )
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def close_assignment(student_id):
        query = (
            "UPDATE counselor_assignments SET status = 'closed' "
            "WHERE student_id = %s AND status = 'active'"
        )
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (student_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

