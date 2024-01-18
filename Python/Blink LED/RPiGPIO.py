import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT,initial=GPIO.LOW)

while True:
    GPIO.output(18,GPIO.HIGH)
    time.sleep(0.000001)
    GPIO.output(18,GPIO.LOW)
    time.sleep(0.000001)