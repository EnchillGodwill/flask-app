import datetime
import os
from http import HTTPStatus

from config import app as flask_app
from config import db
from flask import jsonify, redirect, render_template, request, session, url_for
from flask_cors import CORS
from flask_paginate import get_page_parameter
from models.model import Reading

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
            return redirect(url_for('readings'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['user'] = None
    return redirect(url_for('login'))


@app.route("/send-data", methods=['GET'])
def send_data():
    data = request.args
    created_at = datetime.datetime.now()
    kind, value, device, meta_data = data.get("kind"), data.get(
        "value"), data.get("device"), data.get("meta_data")

    reading = Reading(kind=kind,
                      value=value,
                      device=device,
                      meta_data=meta_data,
                      created_at=created_at)
    db.session.add(reading)
    db.session.commit()
    return jsonify({'message': 'OK'}), HTTPStatus.OK


@app.route("/")
def readings():
    # Authenticate
    if not session.get(
            'user') or session['user'].get('username') != APP_USERNAME:
        return redirect(url_for('login'))

    # Searching
    query = request.args.get('query', "")
    ROWS_PER_PAGE = 400

    page = request.args.get(get_page_parameter(), type=int, default=1)
    readings = Reading.query.filter_by()
    if query:
        readings = readings.filter(Reading.kind.like(f"%{query}%"))
        readings = readings.union(
            Reading.query.filter(Reading.meta_data.like(f"%{query}%")))

    readings = readings.order_by(-Reading.id).paginate(page=page,
                                                       per_page=ROWS_PER_PAGE)

    username = session['user'].get('username')
    payload = {
        "readings": readings,
        "username": username,
        "query": query,
    }
    return render_template("readings.html", **payload)


if __name__ == "__main__":
    app.run()
