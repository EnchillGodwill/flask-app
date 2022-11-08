from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "1234")
POSTGRES_URL = f"{POSTGRES_HOST}:{POSTGRES_PORT}"
POSTGRES_USER = os.environ.get("POSTGRES_USER", "wasp_user")
POSTGRES_PW = os.environ.get("POSTGRES_PW", "wasp_!db_password")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "wasp_db")

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
