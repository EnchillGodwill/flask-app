import datetime
from http import HTTPStatus

from flask import jsonify, redirect, render_template, request, url_for, session
from flask_cors import CORS

from models.model import Reading, TemperatureReading

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
            return redirect(url_for('readings'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['user'] = None
    return redirect(url_for('login'))


@app.route("/post-temperature", methods=['GET'])
def post_temperature():
    data = request.json
    temp = data['temperature']
    temperature = TemperatureReading(temperature=temp,
                                     created_at=datetime.datetime.now())
    db.session.add(temperature)
    db.session.commit()
    return jsonify({'message': 'OK'}), HTTPStatus.OK


@app.route("/post-concentration", methods=['POST'])
def post_concentration():
    data = request.json
    created_at = datetime.datetime.now()
    cal_volt, cal_conc, nit_volt, nit_conc, temp = data['cal_volt'], data[
        'cal_conc'], data['nit_volt'], data['nit_conc'], data.get("temp")

    reading = Reading(cal_conc=cal_conc,
                      cal_volt=cal_volt,
                      nit_volt=nit_volt,
                      nit_conc=nit_conc,
                      temperature=temp,
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

    readings = Reading.query.filter_by().order_by(-Reading.id).all()
    temperature_readings = TemperatureReading.query.filter_by().order_by(
        -TemperatureReading.id).all()

    username = session['user'].get('username')
    payload = {
        "readings": readings,
        "username": username,
        "temperature_readings": temperature_readings,
    }
    return render_template("readings.html", **payload)


if __name__ == "__main__":
    app.run()
