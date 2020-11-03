import RPi.GPIO as gpio
import serial
import time
import os
import watering_functions

def main():
    gpio.setmode(gpio.BOARD)
    gpio.setup(16, gpio.OUT, initial=gpio.HIGH)

    for i in range(0,10):
        try:
            port = serial.Serial(f'/dev/ttyACM{i}')
            print(f'Current port is ACM{i}')
        except:
            print(f'Port {i} is unsuitable')

    elapsed = 0
    start = time.time()
    while True:
        line = port.readline()
        print(line)
        value = float(line[-6:-2])
        elapsed = time.time() - start
        if value > 725 & elapsed > 50: # Higher value means less moisture
            watering_functions.give_water()
            elapsed = 0
            start = time.time()


if __name__ == '__main__':
    try:
        gpio.cleanup()
        main()
    except KeyboardInterrupt:
        gpio.cleanup()
    # except:
    #     os.system('sudo reboot')