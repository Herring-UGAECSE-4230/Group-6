import time
import pigpio
import RPi.GPIO as GPIO
from rotary import Rotary
from read_RPM import reader
from datetime import datetime
import math

# Setup GPIO for RPi.GPIO library
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define pin assignments
clk = 22
dt = 27
sw = 17
ir = 23
motor = 18

# Setup pins
GPIO.setup([clk, dt, sw, ir], GPIO.IN)
GPIO.setup(motor, GPIO.OUT)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize PWM
pwm = GPIO.PWM(motor, 1000)  # Using a 1kHz frequency for the motor control

# Initialize pigpio for encoder and RPM reading
pi = pigpio.pi()
rotations = reader(pi, gpio=ir, pulses_per_rev=3)
my_rotary = Rotary(clk_gpio=clk, dt_gpio=dt, sw_gpio=sw)

# Variables for control logic
pressed = False
rpm_desired = 0
duty = 0
pressCount = 0
lastswState = GPIO.input(sw)

# Encoder handling functions
def cw():
    global rpm_desired, duty, pressed
    if rpm_desired < 5000:
        rpm_desired += 250
        adjust_duty_cycle()

def acw():
    global rpm_desired, duty, pressed
    if rpm_desired > 0:
        rpm_desired -= 250
        adjust_duty_cycle()

def adjust_duty_cycle():
    global duty, pressed
    if rpm_desired > 0:
        duty = max(5, min(95, duty + (rpm_desired // 100)))
        pwm.start(duty)
    else:
        pwm.stop()

def switch_callback():
    global pressed, duty
    if pressed:
        pwm.stop()
    else:
        pwm.start(duty)
    pressed = not pressed
    print("Pressed: ", pressed)

# Setup callbacks for the rotary encoder and switch
my_rotary.setup_rotary(debounce=200, up_callback=acw, down_callback=cw)
my_rotary.setup_switch(debounce=200, long_press=False, sw_short_callback=switch_callback)

# Main loop
try:
    while True:
        current_time = time.time()
        # Print the desired and actual RPM
        actual_rpm = rotations.RPM()  # Get RPM from pigpio reader
        print("Set RPM:", rpm_desired, "Actual RPM:", actual_rpm)
        time.sleep(0.5)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    pi.stop()





