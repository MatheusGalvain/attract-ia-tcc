import os
import mysql.connector

SECRET_KEY = os.environ.get("MY_APP_SECRET_KEY") or os.urandom(24)
API_KEY = "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"
API_CHAT_GPT = "https://api.openai.com/v1/chat/completions"
ID_MODEL = "gpt-3.5-turbo"

db_config = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="db_attract"
)
