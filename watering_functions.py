try: # Try statement is used for testing web server on Macbook, on which the RPi.GPIO library can't be installed
    import RPi.GPIO as gpio
except:
    pass
from datetime import datetime
import time
import serial

gpio.setmode(gpio.BOARD)

def init_output(pin):
    gpio.setup(pin, gpio.OUT, initial=gpio.HIGH)

def give_water(pin=16):
    init_output(pin)
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

def check_reservoir_empty():
    empty = False
    with open('/home/pi/last_watered_log.txt', 'r') as file:
        log = file.readlines()
        try:
            if log[-30][-8:-6] == log[-1][-8:-6]:
                empty = True
            else:
                pass
        except IndexError:
            pass
    return empty

def get_moisture_level_from_sensor(port):
    try:
        line = port.readline()
        value = float(line[-6:-2])
        with open('/home/pi/latest_moisture_level.txt', 'a') as file:
            file.write(f'{datetime.now().strftime("%A %d %B %Y at %H:%M:%S")}: {value}')
    except:
        print('Failed to extract moisture level from sensor')
        pass

def get_moisture_level_from_log():
    try:
        file = open('/home/pi/latest_moisture_level.txt', 'r')
        moisture_level = float(file.readlines()[-1][-4:])
        file.close()
        return moisture_level
    except:
        print("Failed to extract moisture level from log")
        pass

def set_moisture_threshold(level=725):
    with open('/home/pi/moisture_threshold.txt', 'w+') as file:
        file.write(f'{level}')

def get_moisture_threshold():
    file = open('/home/pi/moisture_threshold.txt', 'r')
    threshold = float(file.readlines()[-1])
    file.close()
    return threshold
