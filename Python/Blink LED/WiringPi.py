#Import
import wiringpi
import time

#Set up GPIO and frequency
wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(18)
wiringpi.softToneWrite(18,1)

#Loop to keep the programming running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    wiringpi.softToneWrite(18,0)

        