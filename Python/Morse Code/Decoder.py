import RPi.GPIO as GPIO
import time

# GPIO pin assignments
ledPin = 22
speakerPin = 27
telegraphPin = 17

# Default value for dot, will be calibrated
dot = 0.1
dash = dot * 3
symbol_gap = dot
letter_gap = dot * 3
word_gap = dot * 7
freq = 500
turnOnSpeakerAndLED = True

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(speakerPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(telegraphPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
pwm = GPIO.PWM(speakerPin, freq)  # Corrected to speakerPin for sound output

# Morse code dictionary
MC_Letters = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.', 'h': '....',
    'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
    'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '       ',  # Space
    'attention': '-.-.-', 'over': '-.-', 'out': '.-.-.',
}

Letters_MC = {value: key for key, value in MC_Letters.items()}

# Function definitions

def play_tone(pwm, duration):
    if turnOnSpeakerAndLED:
        pwm.start(50)
        time.sleep(duration)
        pwm.stop()

def output_mc(morse_code):
    for symbol in morse_code:
        if symbol == '.':
            play_tone(pwm, dot)
            time.sleep(symbol_gap)
        elif symbol == '-':
            play_tone(pwm, dash)
            time.sleep(symbol_gap)
        elif symbol == ' ':
            time.sleep(letter_gap)
        else:
            time.sleep(word_gap)

def timeOfPressOrRest(stateOnCall):
    startTime = time.perf_counter()
    if stateOnCall == 1:
        GPIO.wait_for_edge(telegraphPin, GPIO.FALLING)
    else:
        GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
    endTime = time.perf_counter()
    return endTime - startTime

def timeToMorseChar(time, stateOnCall):
    if stateOnCall == 1:
        if time >= (dot * 2):
            return '-'
        else:
            return '.'
    else:
        if time >= (dot * 7):
            return '       '  # Word space
        elif time >= (dot * 2):
            return '   '  # Letter space
        else:
            return ''
    return ''

def determineAverageDotandDash():
    global dot, dash
    dot_times, dash_times = [], []
    
    for _ in range(3):  # Repeat three times for averaging
        GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
        start_time = time.perf_counter()
        GPIO.wait_for_edge(telegraphPin, GPIO.FALLING)
        duration = time.perf_counter() - start_time
        if duration < 0.2:  # Assuming a short press is a dot
            dot_times.append(duration)
        else:  # Assuming a longer press is a dash
            dash_times.append(duration)
    
    dot = sum(dot_times) / len(dot_times) if dot_times else 0.1
    dash = sum(dash_times) / len(dash_times) if dash_times else dot * 3
    print(f"Calibrated dot: {dot}s, dash: {dash}s")

def morse_to_letter(morse):
    return Letters_MC.get(morse, '?')

def decodeUserInput():
    morseInput, decodedWord = "", ""
    stateOnCall = 1  # Assume starting with a press
    while True:
        timeHeld = timeOfPressOrRest(stateOnCall)
        morseChar = timeToMorseChar(timeHeld, stateOnCall)
        if morseChar.strip():
            morseInput += morseChar
            if stateOnCall:  # If previously waiting for release, now wait for press
                stateOnCall = 0
            else:
                decodedLetter = morse_to_letter(morseInput.strip())
                decodedWord += decodedLetter
                morseInput = ""  # Reset for next letter
                if morseChar == "       ":  # End of word
                    break
        stateOnCall = 1 - stateOnCall  # Toggle state
    return decodedWord.strip()

# Main execution

try:
    determineAverageDotandDash()
    print("Ready for Morse code input. Send 'out' to stop.")
    with open("output.txt", "w") as file:
        while True:
            decodedWord = decodeUserInput()
            print(decodedWord)  # Display decoded word
            file.write(decodedWord + "\n")  # Write decoded word to file
            if decodedWord.lower() == "out":
                break
finally:
    GPIO.cleanup()
