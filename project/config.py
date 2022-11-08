from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

SQL_HOST = os.environ.get("SQL_HOST", "localhost")
SQL_PORT = os.environ.get("SQL_PORT", "1234")
POSTGRES_URL = f"{SQL_HOST}:{SQL_PORT}"
POSTGRES_USER = os.environ.get("POSTGRES_USER", "wasp_user")
POSTGRES_PW = os.environ.get("POSTGRES_PW", "wasp_!db_password")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "wasp_db")
DATABASE = os.environ.get("DATABASE", "wasp_db")

if DATABASE == "postgres":
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

# Configure session
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.debug = True

db = SQLAlchemy(app)
