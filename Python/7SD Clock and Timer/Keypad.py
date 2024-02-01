import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressed_key = None

def readLine(line, characters):
    global pressed_key
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(12) == 1:
        pressed_key = characters[0]
    elif GPIO.input(16) == 1:
        pressed_key == characters[1]
    elif GPIO.input(20) == 1:
        pressed_key == characters[2]
    elif GPIO.input(21) == 1:
        pressed_key == characters[3]
    GPIO.output(line, GPIO.LOW)

def read_key ():
    global pressed_key
    pressed_key = None
    time.sleep(0.35)
    for line, char_set in [(18, ["1","2","3","A"]),
                           (23, ["4","5","6","B"]),
                           (24, ["7","8","9","C"]),
                           (25, ["*","0","#","D"])]:
        readLine(line, char_set)
        if pressed_key:
            break
        return pressed_key
try:
    while True:
        key = read_key()
        if key:
            print("Pressed Key: ", key)

except KeyboardInterrupt:
    print("Quitting...")
finally:
    GPIO.cleanup()
