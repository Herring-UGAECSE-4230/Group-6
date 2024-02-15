import RPi._GPIO as GPIO
import time

segment_pins = [17,4,5,6,13,27,22]

GPIO.setmode(GPIO.BCM)

for pin in segment_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)


def test_segements():
    for pin in segment_pins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(2) 
        GPIO.output(pin,GPIO.LOW)

try:
    test_segements()
finally:
    GPIO.cleanup()