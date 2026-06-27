import mysql.connector
from flask import current_app


def get_db_connection():
    config = current_app.config
    return mysql.connector.connect(
        host=config["MYSQL_HOST"],
        user=config["MYSQL_USER"],
        password=config["MYSQL_PASSWORD"],
        database=config["MYSQL_DB"],
        port=config["MYSQL_PORT"],
        auth_plugin="mysql_native_password",
        use_pure=True,
    )
