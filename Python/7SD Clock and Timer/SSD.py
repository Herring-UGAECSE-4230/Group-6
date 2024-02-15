#import libraries
import RPi.GPIO as GPIO
import time


#pins for ssd
segment_pins = [17,4,5,6,13,27,22]

GPIO.setmode(GPIO.BCM)

for pin in segment_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


digit_segments = {
    '0':[1,1,1,1,1,1,0],
    '1':[0,1,1,0,0,0,0],
    '2':[1,1,0,1,1,0,1],
    '3':[1,1,1,1,0,0,1],
    '4':[0,1,1,0,0,1,1],
    '5':[1,0,1,1,0,1,1],
    '6':[1,0,1,1,1,1,1],
    '7':[1,1,1,0,0,0,0],
    '8':[1,1,1,1,1,1,1],
    '9':[1,1,1,0,0,1,1],
    'A':[1,1,1,0,1,1,1],
    'B':[0,0,1,1,1,1,1],
    'C':[1,0,0,1,1,1,0],
    'D':[0,1,1,1,1,0,1],
}

display_on = True

def toggle_display():
    global display_on
    display_on = not display_on
    if not display_on:
    #turn off all
        for pin in segment_pins:
            GPIO.output(pin,GPIO.LOW)


def display_number(digit):
    global display_on
    print(f"dislaying: {digit}, dislaystate:{display_on}")
    if not display_on:
        print("Display is off, not updating ssd")
        return
    if digit =='#':
        toggle_display()
    elif digit in digit_segments:
        for pin, state in zip(segment_pins,digit_segments[digit]):
            GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
    else: 
        for pin in segment_pins:
            GPIO.output(pin, GPIO.LOW)

#GPIO setup for keypad
X = [18,23,24,25]
Y = [12,16,20,21]

for x_pin in X:
    GPIO.setup(x_pin,GPIO.OUT)
for y_pin in Y:
    GPIO.setup(y_pin,GPIO.OUT)

def read_key():
    for rowNum, rowPin in enumerate(X):
        GPIO.output(rowPin,GPIO.HIGH)
        for colNum, colPin in enumerate(Y):
            if GPIO.input(colPin) == 1:
                GPIO.output(rowPin,GPIO.LOW)
                return["1","2","3","4","5","6","7","8","9","A","B","C","D"][rowNum*4 + colNum]
            GPIO.output(rowPin,GPIO.LOW)


try:
    while True:
        key = read_key()
        if key:
            display_number(key)
            time.sleep(0.5)

except KeyboardInterrupt:
    print("\nQuitting")

finally: GPIO.cleanup()










    