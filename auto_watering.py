import RPi.GPIO as gpio
import serial
import time
import os
import watering_functions
import math
import datetime

def main():
    watering_functions.init_output(16)

    for i in range(0,10):
        try:
            port = serial.Serial(f'/dev/ttyACM{i}')
            print(f'Current port is ACM{i}')
            break
        except:
            print(f'Port {i} is unsuitable')

    elapsed = 0
    start = time.time()
    time_to_reboot = (4, 20, 42)
    while True:
        line = port.readline()
        print(line)
        value = float(line[-6:-2])
        elapsed = time.time() - start
        try:
            threshold = watering_functions.get_moisture_threshold()
        except FileNotFoundError:
            threshold = watering_functions.set_moisture_threshold()
        if math.floor(elapsed%30) == 0:
            watering_functions.get_moisture_level_from_sensor(port)
        if value < threshold and elapsed > 1000:
            watering_functions.give_water()
            elapsed = 0
            start = time.time()
            watering_functions.check_reservoir_empty()

        current_date_time = datetime.datetime.now()
        current_time = (current_date_time.hour, current_date_time.minute, current_date_time.second)
        if current_time == time_to_reboot:
            os.system('sudo reboot')

if __name__ == '__main__':
    try:
        gpio.cleanup()
        main()
    except KeyboardInterrupt:
        gpio.cleanup()
    # except:
    #     os.system('sudo reboot')
