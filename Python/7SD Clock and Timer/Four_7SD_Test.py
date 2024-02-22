import time
import RPi.GPIO as GPIO

# GPIO Setup
GPIO.setmode(GPIO.BCM)

# X-Values (Horizontal) Mapping
x_pins = [18, 23, 24, 25]
for pin in x_pins:
    GPIO.setup(pin, GPIO.OUT)

# Y-Values (Vertical) Mapping
y_pins = [12, 16, 20, 21]
for pin in y_pins:
    GPIO.setup(pin, GPIO.IN)

# Clock Setup
clock_pins = [26, 10, 9, 11]
for pin in clock_pins:
    GPIO.setup(pin, GPIO.OUT)

# Seven Segment Setup
segment_pins = [17, 4, 5, 6, 13, 27, 22, 19] #26, 19, 13, 6, 5, 11, 10, 9
for pin in segment_pins:
    GPIO.setup(pin, GPIO.OUT)

LED_pin = 12
GPIO.setup(LED_pin, GPIO.OUT)

enable = True
last_states = {'row1': [], 'row2': [], 'row3': [], 'row4': []}
count = 0

# Resets SSD Display
def reset_GPIO(clock_pin, segment_pins):
    GPIO.output(clock_pin, GPIO.HIGH)
    GPIO.output(segment_pins, GPIO.LOW)
    GPIO.output(clock_pin, GPIO.LOW)

# Conditional implementation of keypad
def read_keypad(row_num, char):
    cur_val = 0
    GPIO.output(row_num, GPIO.HIGH)
    
    for pin in y_pins:
        if GPIO.input(pin) == 1:
            cur_val = char[y_pins.index(pin)]
            time.sleep(0.2)
            break
    
    GPIO.output(row_num, GPIO.LOW)
    return cur_val

try:
    while True:
        GPIO.output(clock_pins, GPIO.LOW)

        # Clock 1 will be used for row 1
        row1 = read_keypad(18, [1, 2, 3, 'A'])
        if enable and row1:
            reset_GPIO(26, segment_pins)
            last_states['row1'] = [4, 5]  # Mapping B, C
            GPIO.output([4, 5], GPIO.HIGH)
            GPIO.output(26, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(26, GPIO.LOW)
        
        # Clock 2 will be used for row 2
        row2 = read_keypad(23, [4, 5, 6, 'B'])
        if enable and row2:
            reset_GPIO(10, segment_pins)
            last_states['row2'] = [5, 6, 13, 27]  # Mapping F, G, B, C
            GPIO.output([5, 6, 13, 27], GPIO.HIGH)
            GPIO.output(10, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(10, GPIO.LOW)

        # Clock 3 will be used for row 3
        row3 = read_keypad(24, [7, 8, 9, 'C'])
        if enable and row3:
            reset_GPIO(9, segment_pins)
            last_states['row3'] = [17, 4, 5, 6, 22]  # Mapping A, B, C, G, D
            GPIO.output([17, 4, 5, 6, 22], GPIO.HIGH)
            GPIO.output(9, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(9, GPIO.LOW)

        # Clock 4 will be used for row 4
        row4 = read_keypad(25, ['*', 0, '#', 'D'])
        if enable and row4 == '#':
            reset_GPIO(11, segment_pins)
            if enable:
                GPIO.output(clock_pins, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(clock_pins, GPIO.LOW)
                enable = False
                time.sleep(0.1)
        elif enable and row4 == 'D':
            reset_GPIO(11, segment_pins)
            count += 1
            GPIO.output(LED_pin, GPIO.HIGH if count % 2 != 0 else GPIO.LOW)
            time.sleep(0.2)
        
except KeyboardInterrupt:
    GPIO.cleanup()
