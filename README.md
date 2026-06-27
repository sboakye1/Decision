# Student Mental Health Resource Decision Support System (DSS)

This repository contains a Flask-based Decision Support System (DSS) built to help universities monitor student well-being, prioritize counseling, and support counselors and administrators with actionable analytics.

## Features

- Authentication for `student`, `counselor`, and `admin` roles
- Monthly mental health survey collection and DSS scoring
- Risk classification (Low / Medium / High) per student survey
- Admin dashboard with assignment workflow and counselor workload balancing
- Counselor case management (notes, appointments)
- Analytics & Insights dashboard with charts and automated insights

## Project Structure

- `app.py` - Flask application factory and entry point
- `config/` - App configuration and environment settings
- `routes/` - Flask blueprints and route handlers
- `services/` - Business logic and data access
- `controllers/` - Request controllers (where implemented)
- `templates/` - Jinja2 HTML templates for UI
- `static/` - CSS and other static assets
- `database/` - Database schema and connection helpers
- `requirements.txt` - Python dependencies

## Installation (Local)

1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Configure environment variables

```powershell
copy .env.example .env
# Edit .env to set SECRET_KEY and MySQL connection values
```

4. Initialize the database

Start your MySQL server and run the provided schema:

```sql
-- from MySQL CLI
SOURCE c:/Users/hp/Desktop/Decision/database/schema.sql;
```

5. Run the app

```powershell
python app.py
```

Open `http://localhost:5000` in your browser.

## Database Setup

- The schema is in `database/schema.sql` and creates normalized tables for users, students, counselors, survey responses and summary, appointments, and counselor assignments/notes.
- The application expects a MySQL database configured in `.env`.

## DSS Explanation (For Presentation)

What is a DSS?

A Decision Support System helps convert raw data into actionable recommendations. This project ingests student survey responses, computes a stress score, classifies risk, and surfaces interventions to administrators and counselors.

How this project implements DSS

- Data collection: Students submit monthly surveys stored in `survey_responses`.
- Scoring: The survey engine aggregates responses into a `total_score` and writes `survey_summary`.
- Risk classification: Thresholds map `total_score` into `Low`, `Medium`, or `High` risk.
- Action: Admins review the analytics and assign counselors to `High`/`Medium` cases.
- Feedback: Counselors record notes and appointments; analytics drive ongoing monitoring.

Risk scoring (high level)

- Each survey response maps to a numeric score.
- Scores are summed to produce a `total_score` per student per month.
- Risk thresholds are configured in code (see `services/survey_service.py`) and convert scores into risk bands.

Decision rules

- Only the most recent survey per student is used for assignment decisions.
- Admins can assign one active counselor per student.
- Counselor workload is monitored; overloaded counselors are highlighted.

## System Flow Page

Visit `/system_flow` (admin-only) for a concise diagram and presentation notes.

## Presentation Tips

- Use the `Admin Analytics` page to show charts and automated insights.
- Highlight the `Assignments` page to demonstrate case workflow and workload balancing.
- Show the `System Flow` page to explain the end-to-end data and decision path.

## Final Notes

This project is prepared for academic demonstration. If you want, I can:

- Add a `docker-compose` to run MySQL + the app locally
- Create a short script to seed demo data for screenshots
- Produce exportable PNG charts for slides

Contact the developer (README author) for any presentation-specific assets.
