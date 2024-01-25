#import
import RPi.GPIO as GPIO
import time
from time import sleep

#Set up GPIO 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT,initial=GPIO.LOW)

#Main Square Wave Loop 
while True:
    GPIO.output(18,GPIO.HIGH)
    time.sleep(0.000005)
    GPIO.output(18,GPIO.LOW)
    time.sleep(0.000005)