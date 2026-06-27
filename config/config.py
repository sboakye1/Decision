import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "replace-with-secure-key")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = os.environ.get("DEBUG", "True") == "True"
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "student_mental_health_dss")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
