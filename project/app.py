import datetime
from http import HTTPStatus

from flask import jsonify, redirect, render_template, request, url_for, session
from flask_cors import CORS

from models.model import Reading

from config import app as flask_app, db
import os

app = flask_app

CORS(app)

APP_USERNAME = os.environ.get("APP_USERNAME", "admin")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "admin")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != APP_USERNAME or request.form[
                'password'] != APP_PASSWORD:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['user'] = {"username": request.form['username']}
            return redirect(url_for('data'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['user'] = None
    return redirect(url_for('login'))


@app.route("/send-data", methods=['GET'])
def send_data():
    data = request.args
    created_at = datetime.datetime.now()
    kind, value, meta_data = data.get("kind"), data.get("value"), data.get(
        "meta_data")

    reading = Reading(kind=kind,
                      value=value,
                      meta_data=meta_data,
                      created_at=created_at)
    db.session.add(reading)
    db.session.commit()
    return jsonify({'message': 'OK'}), HTTPStatus.OK


@app.route("/")
def data():
    # Authenticate
    if not session.get(
            'user') or session['user'].get('username') != APP_USERNAME:
        return redirect(url_for('login'))

    readings = Reading.query.filter_by().order_by(-Reading.id).all()

    username = session['user'].get('username')
    payload = {
        "readings": readings,
        "username": username,
    }
    return render_template("readings.html", **payload)


if __name__ == "__main__":
    app.run()
