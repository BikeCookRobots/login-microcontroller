# login-microcontroller
[video](https://youtu.be/_snGpobyG0U?si=n00AGNiBU5FW5RCM)

Power on and log into your PC over WiFi

Project utilizes a raspberry pi pico w to recieve an MQTT message, simulate a button press, and send keystrokes to input the password.

The 'code.py' file should not need to be changed much, aside from the topics you'd like to publish and subscribe to. 'secrets.py' should contain your various passwords. Only after you've confirmed everything working should you un-comment the lines in 'boot.py' to disable usb mass storage

you may need to adjust the settings on your PC to allow usb devices to stay powered on while the computer is off

# libraries
[minimqtt 7.4.3](https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT/releases/tag/7.4.3)
[HID 6.0.1](https://github.com/adafruit/Adafruit_CircuitPython_HID/releases/tag/6.0.1)
# resources
https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython 
https://learn.adafruit.com/mqtt-in-circuitpython/overview 
https://docs.circuitpython.org/projects/hid/en/latest/examples.html
https://www.microcenter.com/tech_center/article/11343/how-to-prevent-windows-10-from-turning-off-usb-ports-when-asleep
