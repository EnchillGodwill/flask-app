import requests
import serial
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ip_address = '142.93.229.35'
ip_address = 'localhost'
port = 5000

ser = serial.Serial(
    # Serial Port to read the data from
    #    port='/dev/ttyUSB0',
    port='/dev/cu.usbserial-AL032CWB',
    #Rate at which the information is shared to the communication channel
    baudrate=115200,

    # Number of serial commands to accept before timing out
    timeout=1)

while True:
    # Reading all bytes available bytes till EOL
    line = ser.readline()

    if line:
        # Converting Byte Strings into unicode strings
        device_reading = line.decode('utf-8')

        readings = device_reading.replace("\t", "").replace(" ", "").replace(
            "\r", "").replace("\n", "").split("|")
        if len(readings) == 4:
            cal_volt, cal_conc, nit_volt, nit_conc = readings

            # Sending the data to the server
            payload = {
                'cal_volt': cal_volt,
                'cal_conc': cal_conc,
                'nit_volt': nit_volt,
                'nit_conc': nit_conc,
                "temp": 0
            }
            try:
                end_point = f'http://{ip_address}:{port}/post_temp'
                print(f"Posting to : ", end_point)
                r = requests.post(end_point, json=payload)
                print("Status: ", r.status_code)
            except Exception as e:
                print("Failed to send data to server")



@app.route("/temp_records")
def temp_recs():
    df = pd.read_csv('temperature_data.csv', names=['reading', 'createdAt'])
    #df = pd.DataFrame(records, columns=['reading', 'createdAt'])

    fig = px.line(df, y='createdAt', x='reading', title='Temperature Data')
    fig.write_html("templates/temp_recs.html")
    return render_template("temp_recs.html")
