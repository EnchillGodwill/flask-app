import serial
import requests

from flask import Flask
from flask_cors import CORS

app = Flask(__name__) 
CORS(app) 


ip_address = '142.93.229.35'
port = 5000

ser = serial.Serial(
   # Serial Port to read the data from
   port='/dev/ttyUSB0',
    
   #Rate at which the information is shared to the communication channel
   baudrate = 115200,
   
   # Number of serial commands to accept before timing out
   timeout=1
)


while True:
	# Reading all bytes available bytes till EOL
	line = ser.readline()

	if line:
		# Converting Byte Strings into unicode strings
		string = line.decode('utf-8')
		print(string)
		try: 
			temperature_reading = float(string)
		except:
			print(string)
			continue

		payload = {'data': temperature_reading}
		try:
			res = requests.post(f'http://{ip_address}:{port}/post_temp', json=payload)
			print(res.json())
		except Exception as e:
			print(e)
			


@app.route("/temp_records")
def temp_recs():
    df = pd.read_csv('temperature_data.csv', names=['reading', 'createdAt'])
    #df = pd.DataFrame(records, columns=['reading', 'createdAt'])

    fig = px.line(df, y='createdAt', x='reading', title='Temperature Data')
    fig.write_html("templates/temp_recs.html")
    return render_template("temp_recs.html")		
