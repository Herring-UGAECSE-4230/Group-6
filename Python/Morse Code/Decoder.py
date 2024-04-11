import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin Definitions
KEY_PIN = 23  # Telegraph key input
SPEAKER_PIN = 25  # Speaker output
LED_PIN = 24  # LED output

# Setup GPIO pin directions
GPIO.setup(KEY_PIN, GPIO.IN)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

# PWM Setup for Speaker
pwm = GPIO.PWM(SPEAKER_PIN, 500)  # Set PWM to 500Hz

# Morse Code Dictionaries
MORSE_CODE_DICT = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 
                   'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 
                   'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 
                   's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 
                   'y': '-.--', 'z': '--..', ' ': ' ', 'attention': '-.-.-', 'over': '-.-', 
                   'out': '.-.-.', '1': '.----', '0': '-----', '9': '----.-', "sos": "...---...", "?": "?"}

MORSE_TO_LETTERS = {v: k for k, v in MORSE_CODE_DICT.items()}

# Global Variables
dot_length = 0
morse = ""
word = ""
calibrated = False
DEBOUNCE_DELAY = 0.05  # Debounce delay in seconds

# Function to Handle Morse Code Conversion
def handle_morse_code(signal_length):
    global morse, word

    if signal_length < dot_length * 2:
        morse += "."
    elif signal_length >= dot_length * 2:
        morse += "-"

    print(f"Current Morse: {morse}")  # Debug print

# Decode Morse code to letter and reset morse code variable
def decode_morse():
    global morse, word
    character = MORSE_TO_LETTERS.get(morse, "?")
    word += character
    print(f"Decoded Character: {character}")  # Debug print
    morse = ""  # Reset morse code variable

# Calibration Function
def calibrate():
    global dot_length, calibrated
    print("Calibration started. Please input 'attention' in Morse Code (-.-.-).")
    times = []

    for _ in range(5):  # Expecting five signals: dot, dash, dot, dash, dot
        while GPIO.input(KEY_PIN) == GPIO.LOW:
            pass  # Wait for the key press
        time.sleep(DEBOUNCE_DELAY)  # Debounce
        if GPIO.input(KEY_PIN) == GPIO.HIGH:
            GPIO.output(LED_PIN, GPIO.HIGH)  # LED on for visual feedback
            start_time = time.time()
            while GPIO.input(KEY_PIN) == GPIO.HIGH:
                pass  # Wait for release
            GPIO.output(LED_PIN, GPIO.LOW)  # LED off after release
            signal_length = time.time() - start_time
            times.append(signal_length)
            print(f"Signal {len(times)} received.")
    
    # Calculate average dot length from the received signals
    dot_length = sum(times) / len(times)
    calibrated = True
    print(f"Calibration complete. Average signal length (dot length): {dot_length:.3f}s")

# Main Function
def main():
    global morse, word
    calibrate()  # Start with calibration

    try:
        while True:
            input_state = GPIO.input(KEY_PIN)
            if input_state == GPIO.HIGH:  # Key Press Detected
                GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
                time.sleep(DEBOUNCE_DELAY)  # Debouncing
                if GPIO.input(KEY_PIN) == GPIO.HIGH:  # Confirm key press after debounce
                    pwm.start(50)  # Start speaker
                    start_time = time.time()
                    while GPIO.input(KEY_PIN) == GPIO.HIGH:
                        pass  # Wait until key is released
                    pwm.stop()  # Stop speaker
                    GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED
                    signal_length = time.time() - start_time
                    handle_morse_code(signal_length)
                    time.sleep(dot_length)  # Wait for the end of the character
                    decode_morse()  # Decode after each signal to simplify

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
