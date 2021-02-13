import RPi.GPIO as gpio
import time
import os
import watering_functions
import math
import datetime
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn 

def main():
    watering_functions.init_output(23)

    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan = AnalogIn(ads, ADS.P0)    

    elapsed = 0
    start = time.time()
    time_to_reboot = (4, 20, 42)
    while True:
        value = chan.value
        elapsed = time.time() - start
        try:
            threshold = watering_functions.get_moisture_threshold()
        except FileNotFoundError:
            threshold = watering_functions.set_moisture_threshold()
        if math.floor(elapsed%30) == 0:
            watering_functions.write_moisture_to_sqlite(chan)

        time.sleep(.750) # for stabilizing readings from ADC

        if value > threshold and elapsed > 1000:
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
