import RPi.GPIO as GPIO
import simpleaudio as sa
import numpy as np
from time import sleep, perf_counter
import os

# Morse Code Dictionary
MC_DICT = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 
    'y': '-.--', 'z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.', '0': '-----'
}

# GPIO setup
LED_PIN = 17 # Example pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Convert letters to Morse Code
def letter_to_mc(letter):
    return MC_DICT.get(letter.lower(), '')

# Play Morse Code using speaker and LED
def play_mc(code, unit_length):
    for symbol in code:
        if symbol == '.':
            beep_duration = unit_length
        elif symbol == '-':
            beep_duration = 3 * unit_length
        else:
            continue # In case of unexpected character

        # Play beep
        play_beep(beep_duration)
        # Light LED
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
        sleep(beep_duration)

        # Pause between symbols
        GPIO.output(LED_PIN, GPIO.LOW)  # LED OFF
        sleep(unit_length)

def play_beep(duration):
    frequency = 500  # Hz
    fs = 44100  # Sampling frequency
    t = np.linspace(0, duration, int(duration * fs), False)
    note = np.sin(frequency * t * 2 * np.pi)
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    audio = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()

def encode_and_play_messages(file_path, unit_length):
    with open(file_path, 'r') as file:
        lines = [line.rstrip() for line in file.readlines()]
    
    encoded_file_path = 'encoded_messages.txt'
    with open(encoded_file_path, 'w') as encoded_file:
        # Write 'attention' in Morse Code
        attention_mc = ' '.join([letter_to_mc(letter) for letter in 'attention'])
        encoded_file.write(f"{attention_mc} | attention\n")

        for line in lines:
            for word in line.split():
                word_mc = ' '.join([letter_to_mc(letter) for letter in word])
                encoded_file.write(f"{word_mc} | {word}\n")
                play_mc(word_mc, unit_length)
                # Space between words
                sleep(7 * unit_length)
            encoded_file.write('- . - | over\n')
        
        encoded_file.write('. - . - . | out\n')

# Main function
if __name__ == "__main__":
    try:
        unit_length = float(input("Enter the unit length in seconds (e.g., 0.05): "))
        file_path = input("Enter the path to your text file: ")
        encode_and_play_messages(file_path, unit_length)
    finally:
        GPIO.cleanup()