# Imports
from flask import Flask
import RPi.GPIO as GPIO
import time, threading
import adafruit_dht
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from flask_session import Session
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import MySQLdb
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

# MYSQL Database connection
# b = MySQLdb.connect(host="107.23.4.28", port=3306, user="teo", passwd="12345678Qwerty@", db="gms")
db = MySQLdb.connect(host="52.73.218.100", port=3306, user="shaki", passwd="shaki123", db="gms")

# PubNub configuration
pnconfig = PNConfiguration()
# pnconfig.cipher_key = 'myCipherKey'
pnconfig.subscribe_key = 'sub-c-5832596e-d4b6-4552-b2c0-a28a18fadd40'
pnconfig.publish_key = 'pub-c-dab1a887-ba42-48aa-b99d-e42ecf3dedb3'
pnconfig.user_id = "e6f98bfc-65f6-11ed-9022-0242ac120002"
pnconfig.ssl = True  # Encrypt the data when sent to PubNub
pubnub = PubNub(pnconfig)

alive = 0
data = {}
ucl = None

Session(app)
mysql = MySQL(app)
# Setup motion sensor and buzzer pins output
PIR_pin = 23
Buzzer_pin = 24
# GPIO SETUP temperature and humidity pins output
# tmp_sensor = adafruit_dht.DHT11(board.D27, use_pulseio=False)
tmp_sensor = adafruit_dht.DHT11(board.D27)

myChannel = "greenhouse"
tempGraphChannel = "temp-graph"
humGraphChannel = "hum-graph"
pHGraphChannel = "ph-graph"
sensorList = ["buzzer", "temp", "ph", "moisture"]

# GPIO SETUP Motion detection and buzzer pins output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.OUT)

moist_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(moist_pin, GPIO.IN)
# Setup The Ph sensor pins output
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
channel = AnalogIn(ads, ADS.P0)  # Use channel 0 to measure the voltage
# SETUP pins for pump1
in1_p1 = 10
in2_p1 = 9
en_p1 = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1_p1, GPIO.OUT)
GPIO.setup(in2_p1, GPIO.OUT)
GPIO.setup(en_p1, GPIO.OUT)
GPIO.output(in1_p1, GPIO.LOW)
GPIO.output(in2_p1, GPIO.LOW)
p = GPIO.PWM(en_p1, 1000)

# SETUP pins for pump2
in3_p2 = 5
in4_p2 = 6
enB_p2 = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(in3_p2, GPIO.OUT)
GPIO.setup(in4_p2, GPIO.OUT)
GPIO.setup(enB_p2, GPIO.OUT)
GPIO.output(in3_p2, GPIO.LOW)
GPIO.output(in4_p2, GPIO.LOW)
p = GPIO.PWM(enB_p2, 1000)

p.start(100)


def read_temp_ph():  # Function to read the temperature and humidity and Ph
    while True:
        buf = list()
        for i in range(10):  # Take 10 samples
            buf.append(channel.voltage)
        buf.sort()  # Sort samples and discard highest and lowest
        buf = buf[2:-2]  # skip the first two and the last two values
        avg = (sum(map(float, buf)) / 6)  # Get average value from remaining 6 values
        ph_val = (-7.119047 * avg) + (29.14023)  # Calculate the Ph value from the given voltage
        ph_val = round(ph_val, 2)
        publish(myChannel, {"Ph": ph_val})  # Publish the data to PubNub

        print("Ph Buf: ", ph_val)
        # time.sleep(2)

        # fetch the data from UCL table
        if ucl:
            cur = db.cursor()
            cur.execute("select * from data_range where ucl_id=%s", [ucl])
            preset_data = cur.fetchall()

            ph_min = preset_data[0][7]  # The min value will be taken from DB
            ph_max = preset_data[0][8]  # The max value will be taken from DB

            print("from preset", ph_min, ph_max)
            # ph_min = 5.5
            # ph_max = 6.2
            if ph_val < ph_min:
                GPIO.output(in1_p1, GPIO.HIGH)  # The pump turn on
                GPIO.output(in2_p1, GPIO.LOW)
                print("pump1 on - Ph Up")
                time.sleep(5)

                GPIO.output(in1_p1, GPIO.LOW)  # The pump turn off
                GPIO.output(in2_p1, GPIO.LOW)
                print("Pump1 off")
                publish(myChannel, {"Ph_range": "pH too low, pH UP pump on"})
                time.sleep(5)

            elif ph_val > ph_max:
                print("Pump2 On - Ph Down")
                GPIO.output(in3_p2, GPIO.LOW)  # The pump turn on
                GPIO.output(in4_p2, GPIO.HIGH)
                time.sleep(5)

                GPIO.output(in3_p2, GPIO.LOW)  # The pump turn off
                GPIO.output(in4_p2, GPIO.LOW)
                print("Pump2 off")
                publish(myChannel, {"Ph_range": "pH too high, pH DOWN pump on"})
                time.sleep(5)

            else:
                publish(myChannel, {"Ph_range": "pH OK"})

        try:
            if GPIO.input(moist_pin):  # If there is a signal in the pin the moisture is true
                value = "Dry"
                publish(myChannel, {"Soil is": value})  # Publish the data to PubNub
                # print("The soil is dry!")
            else:
                value = "Wet"
                # print("The soil is wet!")
                publish(myChannel, {"Soil is": value})
            # Temperature and humidity data
            temp = tmp_sensor.temperature  # Store the data from the sensor in temp variable
            temp_f = temp * (9 / 5) + 32
            humidity = tmp_sensor.humidity  # Store the data from the sensor in humidity variable
            publish(myChannel, {"atmos": {"temp": temp, "hum": humidity}})  # Publish the data to PubNub

            if ucl:
                cur = db.cursor()
                cur.execute("select * from data_range where ucl_id=%s", [ucl])
                preset_data = cur.fetchall()
                temp_min = preset_data[0][3]  # The min value will be taken from DB
                temp_max = preset_data[0][4]  # The max value will be taken from DB
                hum_min = preset_data[0][5]  # hum_min form DB
                hum_max = preset_data[0][6]  # hum_max from DB

                print("termpHum trest", temp_min, temp_max, hum_min, hum_max)

                if temp < temp_min:
                    publish(myChannel, {"temp_range": "Temperature too low"})
                elif temp > temp_max:
                    publish(myChannel, {"temp_range": "Temperature too high"})
                else:
                    publish(myChannel, {"temp_range": "Temperature OK"})

                if humidity < hum_min:
                    publish(myChannel, {"hum_range": "Humidity too low"})
                elif humidity > hum_max:
                    publish(myChannel, {"hum_range": "Humidity too high"})
                else:
                    publish(myChannel, {"hum_range": "Humidity OK"})

            print("Temp: {:.1f} C / {:.1f} F    Humidity: {}% ".format(temp, temp_f, humidity))

            if ucl:
                cur = db.cursor()
                cur.execute(
                    '''insert into crop_data(ucl_id, creation_dateTime, temp, humidity, pH, moisture) values (%s, %s, %s, %s, %s, %s)''',
                    (ucl, time.strftime('%Y-%m-%d %H:%M:%S'), temp, humidity, ph_val, value))
                db.commit()

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            tmp_sensor.exit()
            raise error
        # time.sleep(10)

def beep(repeat):
    for i in range(0, repeat):
        for pulse in range(60):
            GPIO.output(Buzzer_pin, True)
            time.sleep(0.001)
            GPIO.output(Buzzer_pin, False)
            time.sleep(0.001)
        time.sleep(0.02)

def motion_detection():
    data["alarm"] = False
    print("sensors started")
    trigger = False
    while True:
        if (GPIO.input(PIR_pin)):
            print("Motion detected!")
            beep(4)
            trigger = True
            publish(myChannel, {"motion": "Yes"})
            # TODO: insert to notifications table in database
            if ucl:
                cur = db.cursor()
                cur.execute("select users_id from ucl where ucl_id=%s", [ucl])
                users_id = cur.fetchall()[0][0]
                cur.execute(
                    '''insert into user_notification(notifications_id, users_id, notification_dateTime) values (%s, %s, %s)''',
                    (5, users_id, time.strftime('%Y-%m-%d %H:%M:%S'),))
                db.commit()

            time.sleep(1)
            data["motion"] = 1
        elif trigger:
            publish(myChannel, {"motion": "No"})
            trigger = False
        if data["alarm"]:
            beep(2)
            print("Turning on the buzzer from index.html")
        time.sleep(2)

# PubNub functions
def publish(custom_channel, msg):
    pubnub.publish().channel(custom_channel).message(msg).pn_async(my_publish_callback)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel(myChannel).message('Device connected!').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        try:
            print(message.message)
            msg = message.message
            key = list(msg.keys())
            if key[0] == "event":  # {"event":{"sensor_name" : True}
                self.handleEvent(msg)

            global ucl
            ucl = msg["ucl"]
            print('ucl line 270' + ucl)
        except Exception as e:
            print("Received: ", message.message)
            print(ucl)
            print(e)
            pass

    def handleEvent(self, msg):
        global data
        eventData = msg("event")
        key = list(eventData.keys())
        print(key)
        if key[0] in sensorList:
            if eventData[key[0]] is True:
                data["alarm"] = True
            elif eventData[key[0]] is False:
                data["alarm"] = False

if __name__ == '__main__':
    # Start PubNub Listener
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(myChannel).execute()
    time.sleep(3)

    # Start the threads
    sensors_thread_1 = threading.Thread(target=motion_detection)
    sensors_thread_1.start()
    time.sleep(3)

    sensors_thread_2 = threading.Thread(target=read_temp_ph)
    sensors_thread_2.start()
    time.sleep(3)

    # Run all the thread one after another
    # sensors_thread_1.join()
    # sensors_thread_2.join()
