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

load_dotenv()

app = Flask(__name__)

# PubNub configuration
pnconfig = PNConfiguration()
#pnconfig.cipher_key = 'myCipherKey'
pnconfig.subscribe_key = 'sub-c-5832596e-d4b6-4552-b2c0-a28a18fadd40'
pnconfig.publish_key = 'pub-c-dab1a887-ba42-48aa-b99d-e42ecf3dedb3'
pnconfig.user_id = "e6f98bfc-65f6-11ed-9022-0242ac120002"
pnconfig.ssl = True # Encrypt the data when sent to PubNub
pubnub = PubNub(pnconfig)

myChannel = "greenhouse"
sensorList = ["buzzer"]
# MYSQL Database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'teomeo'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'gms'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
mysql = MySQL(app)
# Setup motion sensor and buzzer pins output
alive = 0
data = {}
PIR_pin = 23
Buzzer_pin = 24
# GPIO SETUP Motion detection and buzzer pins output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_pin, GPIO.IN)
GPIO.setup(Buzzer_pin, GPIO.OUT)

# GPIO SETUP temperature and humidity pins output
tmp_sensor = adafruit_dht.DHT11(board.D17)
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
temp1 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1_p1, GPIO.OUT)
GPIO.setup(in2_p1, GPIO.OUT)
GPIO.setup(en_p1, GPIO.OUT)
GPIO.output(in1_p1, GPIO.LOW)
GPIO.output(in2_p1, GPIO.LOW)
p = GPIO.PWM(en_p1, 1000)

# SETUP pins for pump2
in1_p2 = 5
in2_p2 = 6
en_p2 = 26
temp1 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1_p2, GPIO.OUT)
GPIO.setup(in2_p2, GPIO.OUT)
GPIO.setup(en_p2, GPIO.OUT)
GPIO.output(in1_p2, GPIO.LOW)
GPIO.output(in2_p2, GPIO.LOW)
p = GPIO.PWM(en_p2, 1000)

p.start(100)

def read_ph():  # Function to read the Ph value
    while True:
        buf = list()

        for i in range(10):  # Take 10 samples
            buf.append(channel.voltage)
        buf.sort()  # Sort samples and discard highest and lowest
        buf = buf[2:-2]  # skip the first two and the last two values
        avg = (sum(map(float, buf)) / 6)  # Get average value from remaining 6 values

        ph_val = (-7.119047 * avg) + (29.14023)  # Calculate the Ph value from the given voltage

        # print("avg V: ", round(avg, 2))
        print("Ph Buf: ", round(ph_val, 2))
        publish(myChannel, {"Ph": round(ph_val, 2)})
        time.sleep(2)

        # TODO if the ph is under value run the pump1
        # if ph_val < 4: # if the Ph is less than 7 run the pump1
        #     if (temp1 == 1):
        #         GPIO.output(in1_p1, GPIO.HIGH)
        #         GPIO.output(in2_p1, GPIO.LOW)
        #         print("forward")
        #         time.sleep(5)
        # TODO if the ph is abovr value run the pump2
        # if ph_val > 7: # if the Ph is more than 7 run the pump2
        #     if (temp1 == 1):
        #         GPIO.output(in1_2, GPIO.HIGH)
        #         GPIO.output(in2_2, GPIO.LOW)
        #         print("forward")
        #
def read_temp():  # Function to read the temperature and humidity
    while True:
        try:
            # Detecting the moisture from the soil
            if GPIO.input(moist_pin):
                value = "Dry"
                #print("The soil is dry!")
                publish(myChannel, {"Soil is": value})
            else:
                value = "Wet"
                #print("The soil is wet!")
                publish(myChannel, {"Soil is": value})

            # Temperature and humidity data
            temp = tmp_sensor.temperature
            temp_f = temp * (9 / 5) + 32
            humidity = tmp_sensor.humidity
            #print("Temp: {:.1f} C / {:.1f} F    Humidity: {}% ".format(temp, temp_f, humidity))
            publish(myChannel, {"atmos": {"temp": temp, "hum": humidity}})

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            tmp_sensor.exit()
            raise error
        time.sleep(2)

        # TODO Fix Database connection
        # try:
        # cursor = mysql.connection.cursor()
        # cursor = mysql.connector.connect()
        # cursor.execute("insert into plantdata(creation_dateTime, temp,humidity,ph,moisture) values (%s, %s, %s, %s, %s, %s)",
        #                  time.strfrime('%Y-%m-%d %H:%M:%S '), temp, humidity, 5.5, value)
        # mysql.connection.commit()
        # cursor.close()
        # except mysql.connector.Error as err:
        # print("Something went wrong: {}".format(err))

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
        except Exception as e:
            print("Received: ", message.message)
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
    #Start PubNub Listener
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(myChannel).execute()
    time.sleep(3)

    #Start the threads
    sensors_thread_1 = threading.Thread(target=motion_detection)
    sensors_thread_1.start()

    sensors_thread_2 = threading.Thread(target=read_temp)
    sensors_thread_2.start()

    sensors_thread_3 = threading.Thread(target=read_ph)
    sensors_thread_3.start()



