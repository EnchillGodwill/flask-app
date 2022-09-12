import pymysql.cursors

from application.database
import db 
from application.server  
import app

with app.test_request_context():
	db.init_app(app)
	db.create_all()


def connect_obj():
    return pymysql.connect(host='localhost',
                                 user='root',
                                 password='code@2215Name',
                                 database='libelium',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)


def store_temp(param, reading, created_at):
    # Connect to the database
    connection = connect_obj()

    with connection.cursor() as cursor:
        # Create a new record
        sql = f'''insert into parameter_data (param, reading, createdAt) values ("{param}", "{reading}", "{created_at}")'''
        cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()


def get_temp_data():
    connection = connect_obj()

    with connection.cursor() as cursor:
        # Read a single record
        sql = '''select reading, createdAt from parameter_data'''
        cursor.execute(sql)
        return list(cursor.fetchall())
