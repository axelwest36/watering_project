import RPi.GPIO as gpio
from datetime import datetime
import time

def give_water(pin=16):
    gpio.output(pin, 0)
    time.sleep(1)
    gpio.output(pin, 1)
    with open('/home/pi/last_watered_log.txt', 'a') as file:
            file.write(f'Last watered on: {datetime.now().strftime("%A %d %B %Y at %H:%M:%S")}')

def get_last_watered():
    file = open('/home/pi/last_watered_log.txt', 'r')
    log = file.readlines()
    file.close()
    return log[-1]


