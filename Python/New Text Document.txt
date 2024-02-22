import RPi.GPIO as GPIO
import time
import random

# Setup
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the SSD segments and clocks
clock_pins = [26, 10, 9, 11]  # Clock pins for each of the 4 SSDs
segment_pins = [17, 4, 5, 6, 13, 27, 22, 19]  # A, B, C, D, E, F, G, DP

# Setup the segment and clock pins
for pin in segment_pins + clock_pins:
    GPIO.setup(pin, GPIO.OUT)

# Character to segments mapping for SSDs (0-9, A-D, *, #)
char_to_segments = {
    '0': [0, 1, 2, 3, 4, 5],
    '1': [1, 2],
    '2': [0, 1, 6, 4, 3],
    '3': [0, 1, 6, 2, 3],
    '4': [5, 6, 1, 2],
    '5': [0, 5, 6, 2, 3],
    '6': [0, 5, 4, 3, 2, 6],
    '7': [0, 1, 2],
    '8': [0, 1, 2, 3, 4, 5, 6],
    '9': [0, 1, 5, 6, 2],
    'A': [0, 1, 2, 5, 6, 4],
    'B': [5, 4, 3, 2, 6],
    'C': [0, 5, 4, 3],
    'D': [1, 2, 3, 4, 6],
    '*': [7],  # Assuming DP represents the dot
    '#': []
}

def display_char(ssd_index, char):
    """Displays a character on one of the SSDs."""
    # Clear all segments
    for pin in segment_pins:
        GPIO.output(pin, GPIO.LOW)
    
    # Activate the relevant segments for this character
    for segment_index in char_to_segments[char]:
        GPIO.output(segment_pins[segment_index], GPIO.HIGH)

    # Turn on the relevant SSD clock for a short time to display the character
    GPIO.output(clock_pins[ssd_index], GPIO.HIGH)
    time.sleep(0.5)  # Display for half a second
    GPIO.output(clock_pins[ssd_index], GPIO.LOW)

try:
    while True:
        # Randomly select a character to display on each SSD
        for i in range(4):
            char = random.choice(list(char_to_segments.keys()))
            display_char(i, char)
        time.sleep(1)  # Wait for 1 second before the next update

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO states on exit