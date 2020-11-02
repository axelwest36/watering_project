import RPi.GPIO as gpio
import serial
from time import sleep

gpio.setmode(gpio.BOARD)
gpio.setup(16, gpio.OUT, initial=gpio.HIGH)
gpio.output(16, 1)

for i in range(0,10):
    try:
        port = serial.Serial(f'/dev/ttyACM{i}')
        print(f'Current port is ACM{i}')
    except:
        print(f'Port {i} is unsuitable')

def give_water():
    gpio.output(16, 0)
    sleep(1)
    gpio.output(16, 1)
    sleep(50)


while True:
    line = port.readline()
    print(line)
    value = float(line[-6:-2])
    if value > 725: # Higher value means less moisture
        give_water()

