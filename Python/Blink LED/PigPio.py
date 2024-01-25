#Import
import pigpio
import time

#Set up GPIO, Set frequency/duty-cycle
pi = pigpio.pi()
pi.set_PWM_frequency(18,20000)
pi.set_PWM_dutycycle(18,128)

#Loop to keep the program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pi.set_PWM_frequency(18,0)

