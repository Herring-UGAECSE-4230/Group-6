import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
channel = 18 # GPIO 18 is used
GPIO.setup(channel, GPIO.OUT)

print("Enter Frequency:")
freq = int(input())
print("Enter Duty cycle: ")
duty = int(input())

# Set up PWM
pwm = GPIO.PWM(channel, freq)

try:
    while True:
        pwm.ChangeFrequency(freq)
        pwm.start(duty)


except KeyboardInterrupt:
    # Clean up on keyboard interrupt
    pwm.stop()
    GPIO.cleanup()
