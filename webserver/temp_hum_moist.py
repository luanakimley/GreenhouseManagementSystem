import time
import board
import adafruit_dht
import psutil
import RPi.GPIO as GPIO
import time
# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
#GPIO SETUP
tmp_sensor = adafruit_dht.DHT11(board.D17)
moist_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(moist_pin, GPIO.IN)



while True:
    try:
        temp = tmp_sensor.temperature
        temp_f = temp * (9 / 5) + 32
        humidity = tmp_sensor.humidity
        print("Temp: {:.1f} C / {:.1f} F    Humidity: {}% "
               .format(temp, temp_f, humidity))
        if GPIO.input(moist_pin):
            print ("dry!")
        else:
            print ("wet!")       
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        tmp_sensor.exit()
        raise error
    time.sleep(2.0)
    
