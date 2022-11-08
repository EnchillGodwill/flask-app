
from datetime import datetime

import pymysql


class Database(object):
    
    libeliumconnection = None
    libeliumcursor = None
    
    
    def __init__(self, libhost='localhost', libdatabase = 'libelium', libuser = 'libelium', libpassword='icui4cu.'):
        # self.libeliumconnection = pymysql.connect(host=libhost, user=libuser, password=libpassword, database=libdatabase)
        # self.libeliumcursor = self.libeliumconnection.cursor()
        pass
        
        
    def record_temperature(self, temperature):
        pass
        # created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # sql_statement = f"INSERT INTO ParameterData (param, reading, createdAt) VALUES ( 'Temperature', {temperature}, '{created_at}' )"
        
        # #print(sql_statement)
        
        # self.libeliumcursor.execute(sql_statement)
        # self.libeliumconnection.commit()
        # self.libeliumconnection.close()
