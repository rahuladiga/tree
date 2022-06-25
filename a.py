from mpu6050 import mpu6050
import pyrebase
from time import sleep
import random
import serial
import sys
config = {     
  "apiKey": "AIzaSyBz9r4zM0cgw8XYIqCbR8gsnJHGl45rqxk",
  "authDomain": "ehgh-46b01.firebaseapp.com",
  "databaseURL": "https://ehgh-46b01.firebaseio.com",
  "storageBucket": "ehgh-46b01.appspot.com"
}
ser = serial.Serial ("/dev/ttyAMA0")
gpgga_info = "$GPGGA,"
GPGGA_buffer = 0
NMEA_buff = 0
sensor = mpu6050(0x68)
firebase = pyrebase.initialize_app(config)
db = firebase.database()
lat
longi
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

def getGpsData():
    try:
        received_data = (str)(ser.readline()) #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string
            NMEA_buff = (GPGGA_buffer.split(','))
            nmea_time = []
            nmea_latitude = []
            nmea_longitude = []
            nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
            nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
            nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
            print("Time: ", nmea_time,'\n')
            lat = (float)(nmea_latitude)
            lat = convert_to_degrees(lat)
            longi = (float)(nmea_longitude)
            longi = convert_to_degrees(longi)
            print ("Latitude:", lat,"Longitude:", longi,'\n')      
    except:
        lat=13.254648632394062
        longi=74.78524044824572
        print ("Latitude:", lat,"Longitude:", longi,'\n')

try:
    while True:
        accelerometer_data = sensor.get_accel_data()
        print("X="+str(accelerometer_data.get('x'))+", Y="+str(accelerometer_data.get('y'))+", Z="+str(accelerometer_data.get('z')))
        if(-5>accelerometer_data.get('x')>5 and -5>accelerometer_data.get('y')>5):
            db.child("data").update({"gyroData":"X="+str(accelerometer_data.get('x'))+", Y="+str(accelerometer_data.get('y'))+", Z="+str(accelerometer_data.get('z'))})
            getGpsData()
            db.child("data").update({"gpsData": "Latitude:"+lat+" Longitude:"+longi})
            db.child("data").update({"alert":  random.random()})
except:
    print("err")