import time
import RPi.GPIO as GPIO

# Defining GPIO mode
GPIO.setmode(GPIO.BCM)

# GPIO pin setup
# X-Values (Horizontal) for keypad
X_PINS = [18, 23, 24, 25]  # Yellow, Orange, Brown, Red wires
# Y-Values (Vertical) for keypad
Y_PINS = [12, 16, 20, 21]  # Black, White, Gray, Blue wires
# GPIO pins for the SSD
SSD_PINS = [17, 4, 6, 13, 19, 27, 22, 5, 26]  # A, B, C, D, E, F, G, DP, Clk

# Setup GPIO pins
for pin in X_PINS + Y_PINS + SSD_PINS:
    GPIO.setup(pin, GPIO.OUT if pin in X_PINS or pin in SSD_PINS else GPIO.IN)

enable = True

# Mapping of digits to GPIO states for SSD
DIGIT_MAP = {
    0: [1,1,1,1,1,1,0],
    1: [0,1,1,0,0,0,0],
    2: [1,1,0,1,1,0,1],
    3: [1,1,1,1,0,0,1],
    4: [0,1,1,0,0,1,1],
    5: [1,0,1,1,0,1,1],
    6: [1,0,1,1,1,1,1],
    7: [1,1,1,0,0,0,0],
    8: [1,1,1,1,1,1,1],
    9: [1,1,1,1,0,1,1]
}

def reset_ssd():
    """ Resets the SSD display. """
    GPIO.output(SSD_PINS[-1], GPIO.HIGH)  # Clk High
    for pin in SSD_PINS[:-1]:
        GPIO.output(pin, GPIO.LOW)
    GPIO.output(SSD_PINS[-1], GPIO.LOW)   # Clk Low

def read_keypad():
    """ Reads the keypad and returns the pressed key, if any. """
    key_map = [
        [1, 2, 3, 'A'],
        [4, 5, 6, 'B'],
        [7, 8, 9, 'C'],
        ['*', 0, '#', 'D']
    ]
    for x_pin, row in zip(X_PINS, key_map):
        GPIO.output(x_pin, GPIO.HIGH)
        for y_pin, key in zip(Y_PINS, row):
            if GPIO.input(y_pin) == 1:
                time.sleep(0.2)
                GPIO.output(x_pin, GPIO.LOW)
                return key
        GPIO.output(x_pin, GPIO.LOW)
    return None

def display_digit(digit):
    """ Displays a digit on the SSD. """
    if digit in DIGIT_MAP:
        for pin, state in zip(SSD_PINS[:-1], DIGIT_MAP[digit]):
            GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
        GPIO.output(SSD_PINS[-1], GPIO.HIGH)  # Clk High
        time.sleep(0.1)
        GPIO.output(SSD_PINS[-1], GPIO.LOW)   # Clk Low

try:
    while True:
        reset_ssd()
        key = read_keypad()
        if key is not None:
            if isinstance(key, int) and enable:
                display_digit(key)
            elif key == '#':
                enable = not enable
except KeyboardInterrupt:
    GPIO.cleanup()