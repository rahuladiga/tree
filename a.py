from mpu6050 import mpu6050
from time import sleep 
sensor = mpu6050(0x68)
while(1):
    accelerometer_data = sensor.get_accel_data()
    sleep(1)
    print("X="+str(accelerometer_data.get('x'))+"Y="+str(accelerometer_data.get('y'))+
          "Z="+str(accelerometer_data.get('z')))