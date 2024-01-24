import pigpio
import time

pi = pigpio.pi()
pi.set_PWM_frequency(18,150)
pi.set_PWM_dutycycle(18,128)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pi.set_PWM_frequency(18,0)

