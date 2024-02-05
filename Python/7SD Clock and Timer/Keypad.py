#import libraries
import RPi.GPIO as GPIO
import time

#Horizontal Mapping Values
X1 = 18
X2 = 23
X3 = 24
X4 = 25

#Vertical Mapping Values
Y1 = 12
Y2 = 16
Y3 = 20 
Y4 = 21

#setup GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(X1, GPIO.OUT)
GPIO.setup(X2, GPIO.OUT)
GPIO.setup(X3, GPIO.OUT)
GPIO.setup(X4, GPIO.OUT)
GPIO.setup(Y1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Y2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Y3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Y4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#main keypad loop
def readKey(rowNum, char):
    curVal = 0
    GPIO.output(rowNum, GPIO.HIGH)
    if GPIO.input(Y1) == 1:
        curVal = char[0]
        print (curVal)
    if GPIO.input(Y2) == 1:
        curVal = char[1]
        print (curVal)
    if GPIO.input(Y3) == 1:
        curVal = char[2]
        print (curVal)
    if GPIO.input(Y4) == 1:
        curVal = char[3]
        print (curVal)
    GPIO.output(rowNum, GPIO.LOW)

try:
    while True:
        readKey (X1, ["1","2","3","A"])
        time.sleep(0.1)
        readKey (X2, ["4","5","6","B"])
        time.sleep(0.1)
        readKey (X3, ["7","8","9","C"])
        time.sleep(0.1)
        readKey (X4, ["*","0","#","D"])
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nQuitting")