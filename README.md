# Student Mental Health Resource Decision Support System (DSS)

This project is a Flask-based decision support system designed to help universities identify students who may need mental health support, prioritize counseling appointments, and assist counselors in making decisions based on academic performance, attendance, and monthly survey responses.

## Project Structure

- `app.py`: Flask application entry point and factory function.
- `config/config.py`: Application configuration class loaded from environment variables.
- `requirements.txt`: Python package dependencies.
- `.env.example`: Template environment variables for local development.
- `templates/`: HTML templates for the frontend pages.
- `static/`: Static assets such as CSS, JS, and images.
- `routes/`: Route definitions and blueprint registration.
- `controllers/`: Request handling and business flow controllers.
- `models/`: Data model definitions and ORM integration.
- `services/`: Reusable domain and application services.
- `database/`: Database connection and initialization logic.
- `utils/`: Utility helpers shared across the application.
- `config/`: Configuration management.

## Installation

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the Project

1. Copy `.env.example` to `.env` and update values.
2. Start the Flask app:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` in your browser.

## Notes

- The current scaffold does not include authentication or database tables.
- Add models, controllers, and routes incrementally in their respective folders.
