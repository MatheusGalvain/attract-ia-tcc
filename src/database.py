import mysql.connector
from config import db_config


def get_user_data(user_id):
    with mysql.connector.connect(**db_config) as db_connection:
        db_cursor = db_connection.cursor(dictionary=True)
        db_cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
        resultado = db_cursor.fetchone()
        db_cursor.close()
    return resultado
