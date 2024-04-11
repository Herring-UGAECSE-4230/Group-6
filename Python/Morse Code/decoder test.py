import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO Setup for Input, Output, PWM, and LED
GPIO.setup(23, GPIO.IN)  # Telegraph key as input
GPIO.setup(25, GPIO.OUT)  # Speaker as output
GPIO.setup(24, GPIO.OUT)  # LED as output
pwm = GPIO.PWM(25, 500)  # Initialize PWM on pin 25 at 500Hz
GPIO.output(24, GPIO.LOW)  # Ensure LED is off at start

# Morse Code Dictionaries
MORSE_CODE_DICT = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 
    'y': '-.--', 'z': '--..', ' ': ' ', 'attention': '-.-.-', 'over': '-.-',
    'out': '.-.-.', '1': '.----', '0': '-----', '9': '----.-', "sos": "...---...", "?":"?"
}

MORSE_TO_LETTERS = {
    '.-':'a', '-...':'b', '-.-.':'c', '-..':'d', '.':'e', '..-.':'f', 
    '--.':'g', '....':'h', '..':'i', '.---':'j', '-.-':'k', '.-..':'l', 
    '--':'m', '-.':'n', '---':'o', '.--.':'p', '--.-':'q', '.-.':'r', 
    '...':'s', '-':'t', '..-':'u', '...-':'v', '.--':'w', '-..-':'x', 
    '-.--':'y', '--..':'z', ' ': ' ', '-.-.-':'attention', '-.-':'over',
    '.-.-.':'out', '.----':'1', '-----':'0', '----.-':'9', "...---...": "sos", "?":"?"
}

# Global variables initialization
dot_length = 0
morse = ""
word = ""
calibrated = False

def encode():
    global word
    outputfile = open("output.txt", "w")
    mc = ""
    word_array = word.split("\n")
    
    for x in word_array:   
        if x == "attention":
            mc += "-.-.-"
        elif x == "over":
            mc += "-.-"
        elif x == "out":
            mc += ".-.-."
        else:
            for char in x:
                mc += MORSE_CODE_DICT.get(char, "?") + " "
        mc += "| " + x + "\n"
    
    outputfile.write(mc[:-1])
    outputfile.close()

def calibrate():
    global calibrated, dot_length, word
    count = 0
    print("Tap: -.-.-")
    while not calibrated:
        if GPIO.input(23) == 1:
            GPIO.output(24, GPIO.HIGH)  # Turn on LED when key is pressed
            pwm.start(50)
            time.sleep(0.05)
            
            if count == 0:
                dash_start = time.time()
            elif count in (1, 3):
                dot_start = time.time()
            elif count in (2, 4):
                dash_start = time.time()

            while GPIO.input(23) == 1:
                pass
            GPIO.output(24, GPIO.LOW)  # Turn off LED when key is released
            time.sleep(0.01)
            count += 1
            
        elif GPIO.input(23) == 0:
            pwm.stop()
            if count == 1:
                first_dash = time.time() - dash_start
            elif count == 2:
                first_dot = time.time() - dot_start
            elif count == 3:
                second_dash = time.time() - dash_start
            elif count == 4:
                second_dot = time.time() - dot_start
            elif count == 5:
                third_dash = time.time() - dash_start
                calibrated = True

    dot_length = (first_dash + second_dash + third_dash) / 9
    print("Calibration complete. Unit dot length is:", dot_length)
    word += "attention\n"

calibrate()
print("Calibrated")

while True:
    if GPIO.input(23) == 1:  # Key press detected
        GPIO.output(24, GPIO.HIGH)  # Turn on LED
        on = time.time()
        pwm.start(50)
        
        while GPIO.input(23) == 1:  # Wait while key is pressed
            pass

        GPIO.output(25, 0)  # Turn off speaker
        GPIO.output(24, GPIO.LOW)  # Turn off LED
        onLength = time.time() - on  # Calculate press duration
        
        # Determine if the signal is a dot or dash based on duration
        if onLength < dot_length * 2 and onLength > 0.01:
            morse += "."
        elif onLength > dot_length * 2:
            morse += "-"

    elif GPIO.input(23) == 0:  # Key release detected
        pwm.stop()
        off = time.time()
        
        while GPIO.input(23) == 0:  # Wait while key is not pressed
            GPIO.output(25, 0)
        
        offLength = time.time() - off  # Calculate release duration
        
        # Handle inter-character and inter-word spaces
        if offLength > dot_length * 6:  # Space between words
            if morse in MORSE_TO_LETTERS:
                character = MORSE_TO_LETTERS[morse]
                word += character + "\n"
                morse = ""
                print(word)
                if character == "out":
                    encode()
                    break
            elif morse:
                word += "?\n"
                morse = ""

import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO Setup for Input, Output, PWM, and LED
GPIO.setup(23, GPIO.IN)  # Telegraph key as input
GPIO.setup(25, GPIO.OUT)  # Speaker as output
GPIO.setup(24, GPIO.OUT)  # LED as output
pwm = GPIO.PWM(25, 500)  # Initialize PWM on pin 25 at 500Hz
GPIO.output(24, GPIO.LOW)  # Ensure LED is off at start

# Morse Code Dictionaries
MORSE_CODE_DICT = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 
    'y': '-.--', 'z': '--..', ' ': ' ', 'attention': '-.-.-', 'over': '-.-',
    'out': '.-.-.', '1': '.----', '0': '-----', '9': '----.-', "sos": "...---...", "?":"?"
}

MORSE_TO_LETTERS = {
    '.-':'a', '-...':'b', '-.-.':'c', '-..':'d', '.':'e', '..-.':'f', 
    '--.':'g', '....':'h', '..':'i', '.---':'j', '-.-':'k', '.-..':'l', 
    '--':'m', '-.':'n', '---':'o', '.--.':'p', '--.-':'q', '.-.':'r', 
    '...':'s', '-':'t', '..-':'u', '...-':'v', '.--':'w', '-..-':'x', 
    '-.--':'y', '--..':'z', ' ': ' ', '-.-.-':'attention', '-.-':'over',
    '.-.-.':'out', '.----':'1', '-----':'0', '----.-':'9', "...---...": "sos", "?":"?"
}

# Global variables initialization
dot_length = 0
morse = ""
word = ""
calibrated = False

def encode():
    global word
    outputfile = open("output.txt", "w")
    mc = ""
    word_array = word.split("\n")
    
    for x in word_array:   
        if x == "attention":
            mc += "-.-.-"
        elif x == "over":
            mc += "-.-"
        elif x == "out":
            mc += ".-.-."
        else:
            for char in x:
                mc += MORSE_CODE_DICT.get(char, "?") + " "
        mc += "| " + x + "\n"
    
    outputfile.write(mc[:-1])
    outputfile.close()

def calibrate():
    global calibrated, dot_length, word
    count = 0
    print("Tap: -.-.-")
    while not calibrated:
        if GPIO.input(23) == 1:
            GPIO.output(24, GPIO.HIGH)  # Turn on LED when key is pressed
            pwm.start(50)
            time.sleep(0.05)
            
            if count == 0:
                dash_start = time.time()
            elif count in (1, 3):
                dot_start = time.time()
            elif count in (2, 4):
                dash_start = time.time()

            while GPIO.input(23) == 1:
                pass
            GPIO.output(24, GPIO.LOW)  # Turn off LED when key is released
            time.sleep(0.01)
            count += 1
            
        elif GPIO.input(23) == 0:
            pwm.stop()
            if count == 1:
                first_dash = time.time() - dash_start
            elif count == 2:
                first_dot = time.time() - dot_start
            elif count == 3:
                second_dash = time.time() - dash_start
            elif count == 4:
                second_dot = time.time() - dot_start
            elif count == 5:
                third_dash = time.time() - dash_start
                calibrated = True

    dot_length = (first_dash + second_dash + third_dash) / 9
    print("Calibration complete. Unit dot length is:", dot_length)
    word += "attention\n"

calibrate()
print("Calibrated")

while True:
    if GPIO.input(23) == 1:  # Key press detected
        GPIO.output(24, GPIO.HIGH)  # Turn on LED
        on = time.time()
        pwm.start(50)
        
        while GPIO.input(23) == 1:  # Wait while key is pressed
            pass

        GPIO.output(25, 0)  # Turn off speaker
        GPIO.output(24, GPIO.LOW)  # Turn off LED
        onLength = time.time() - on  # Calculate press duration
        
        # Determine if the signal is a dot or dash based on duration
        if onLength < dot_length * 2 and onLength > 0.01:
            morse += "."
        elif onLength > dot_length * 2:
            morse += "-"

    elif GPIO.input(23) == 0:  # Key release detected
        pwm.stop()
        off = time.time()
        
        while GPIO.input(23) == 0:  # Wait while key is not pressed
            GPIO.output(25, 0)
        
        offLength = time.time() - off  # Calculate release duration
        
        # Handle inter-character and inter-word spaces
        if offLength > dot_length * 6:  # Space between words
            if morse in MORSE_TO_LETTERS:
                character = MORSE_TO_LETTERS[morse]
                word += character + "\n"
                morse = ""
                print(word)
                if character == "out":
                    encode()
                    break
            elif morse:
                word += "?\n"
                morse = ""

