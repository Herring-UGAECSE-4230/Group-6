#import libraries
import RPi.GPIO as GPIO
import time
import Keypad

#pins for ssd
segment_pins = [17,4,5,6,13,27,22]

GPIO.setmode(GPIO.BCM)

for pin in segment_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)




digit_segments = {
    '0':[1,1,1,1,1,1,0],
    '1':[0,1,1,0,0,0,0],
    '2':[1,1,0,1,1,0,1],
    '3':[1,1,1,1,0,0,1],
    '4':[0,1,1,0,0,1,1],
    '5':[1,0,1,1,0,1,1],
    '6':[1,0,1,1,1,1,1],
    '7':[1,1,1,0,0,0,0],
    '8':[1,1,1,1,1,1,1],
    '9':[1,1,1,0,0,1,1],
    'A':[1,1,1,0,1,1,1],
    'B':[0,0,1,1,1,1,1],
    'C':[1,0,0,1,1,1,0],
    'D':[0,1,1,1,1,0,1],
}

def display_number(digit):
    if digit in digit_segments:
        for pin, state in zip(segment_pins,digit_segments[digit]):
            GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
        else: 
            for pin in segment_pins:
                GPIO.output(pin, GPIO.LOW)

try:
    while True:
        key = Keypad.readKey()
        if key is not None:
            if key == '#': 
                display_number(key)
            else :display_number(key)
            time.sleep(0.5)

except KeyboardInterrupt:
    print("\nQuitting")

finally: GPIO.cleanup()










    