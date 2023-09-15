import os
import mysql.connector

SECRET_KEY = os.environ.get("MY_APP_SECRET_KEY") or os.urandom(24)

db_config = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_attract"
)
