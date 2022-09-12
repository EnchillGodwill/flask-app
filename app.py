from flask import Flask, request, jsonify, render_template, url_for
from http import HTTPStatus

import serial, datetime
from db import store_temp, get_temp_data

import plotly.express as px
import pandas as pd


from flask_cors import CORS 
app = Flask(__name__)
CORS(app) 

@app.route("/")
def index():
    return jsonify({'message': 'OK'}), HTTPStatus.OK

@app.route("/post_temp", methods=['POST'])
def post_temp():
    json_ = request.json
    data = json_['data']

    param = 'Temperature'
    reading = data
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #store_temp(param, reading, created_at)

    with open('temperature_data.csv', 'a+') as f:
        f.write(f"{created_at}, {reading}\n")

    return jsonify({'message': 'OK'}), HTTPStatus.OK


@app.route("/temp_records")
def temp_recs():
    df = pd.read_csv('temperature_data.csv', names=['reading', 'createdAt'])
    #df = pd.DataFrame(records, columns=['reading', 'createdAt'])

    fig = px.line(df, y='createdAt', x='reading', title='Temperature Data')
    fig.write_html("templates/temp_recs.html")
    return render_template("temp_recs.html")
