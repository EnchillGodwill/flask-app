import requests
import serial
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

server_address = "https://enchill.pythonanywhere.com"
server_address = "http://localhost:5000"
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

        # readings = device_reading.replace("\t", "").replace(" ", "").replace(
        #     "\r", "").replace("\n", "").split("|")

        print("device_reading", device_reading)

        # Sending the data to the server
        payload = {
            'kind': "temperature",
            'value': 44.2,
            'meta_data': "Location: Akosombo",
        }
        # try:
        #     end_point = f'{server_address}/send-data'
        #     print(f"Posting to : ", end_point)
        #     r = requests.get(end_point, params=payload)
        #     print("Status: ", r.status_code)
        # except Exception as e:
        #     print("Failed to send data to server")
