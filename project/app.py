import datetime
from http import HTTPStatus

from flask import jsonify, render_template, request
from flask_cors import CORS

from models.model import Reading

from config import app as flask_app, db

app = flask_app

CORS(app)


@app.route("/")
def index():
    return jsonify({'message': 'OK'}), HTTPStatus.OK


@app.route("/temperature", methods=['GET'])
def record_temperature():
    # temperature = request.args.get("reading")
    # db = Database()
    # db.record_temperature(temperature)

    return jsonify({'message': 'OK'}), HTTPStatus.OK


@app.route("/post_temp", methods=['POST'])
def post_temp():
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


@app.route("/readings")
def temp_recs():
    readings = Reading.query.filter_by().order_by(-Reading.id).all()
    payload = {"readings": readings}
    return render_template("readings.html", **payload)


if __name__ == "__main__":
    app.run()
