import os

SECRET_KEY = os.environ.get("MY_APP_SECRET_KEY") or os.urandom(24)

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'db_attract',
}
