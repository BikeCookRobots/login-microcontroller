import board
import digitalio
from secrets import secrets
import time

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS 
import adafruit_minimqtt.adafruit_minimqtt as MQTT

import socketpool
import wifi

# topics you will communicate over. Change these to whatever you like
cmd_topic = "/test/topic/cmd"
stat_topic = "/test/topic/stat"

# setup IO pins
led = digitalio.DigitalInOut(board.LED) #LED to show activity. Not required
led.direction = digitalio.Direction.OUTPUT

transistor = digitalio.DigitalInOut(board.GP3)
transistor.direction = digitalio.Direction.OUTPUT

# connect to wifi
wifi.radio.connect(secrets["ssid"], secrets["AP_password"])
pool = socketpool.SocketPool(wifi.radio)

# set up a mqtt client
mqtt_client = MQTT.MQTT(
    broker=secrets["broker"],
    username=secrets["mqtt_user"],
    password=secrets["mqtt_pass"],
    port=secrets["port"],
    socket_pool=pool
)

def initiateKeyboard():
    global kbd, layout
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)

def message(client, topic, message):
    if message == "on":
        mqtt_client.publish(stat_topic, "pressed")
        shortPress() # bridges the power button pins
        time.sleep(40) # this time should reflect how long it takes to get to the login screen

        # if kbd is not defined, then initiate it
        # we have to do this after the computer powers on, because the keyboard library doesnt work until the data is active
        # i dont totally get it tbh
        try:
            kbd
        except NameError:
            initiateKeyboard()

        kbd.send(Keycode.CONTROL) # this is to dismiss the lock screen
        time.sleep(1)
        sendLogin()
        mqtt_client.publish(stat_topic, "ready")

    else:
        mqtt_client.publish(stat_topic, "unknown command")
        time.sleep(15)
        mqtt_client.publish(stat_topic, "ready")

# input function definitions
def shortPress():
    led.value = True
    transistor.value = True
    time.sleep(1)
    transistor.value = False
    led.value = False

def sendLogin():
    # write password
    # place plaintext password in "secrets.py" under "computer_password"
    layout.write(secrets["computer_password"],0.1)
    kbd.send(Keycode.ENTER)
    mqtt_client.publish(stat_topic, "input sent")

    
# connect mqtt callbacks
mqtt_client.on_message = message
mqtt_client.connect()

mqtt_client.subscribe(cmd_topic)
mqtt_client.publish(stat_topic, "ready")

while True:
    mqtt_client.loop()
    