import wiringpi
import time

wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(18)
wiringpi.softToneWrite(18,0.1)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    wiringpi.softToneWrite(18,0)

        