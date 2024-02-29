import RPi.GPIO as GPIO
import time
from datetime import datetime


# Pin Definitions
led_pin = 12
clock_pins = [26,10,9,11]
data_pins = [17,4,5,6,13,27,22,19]
# Clock Setup
Clk1 = 26
Clk2 = 10
Clk3 = 9
Clk4 = 11
# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)
for pin in data_pins + clock_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
# Global Variables
current_time = [0, 0, 0, 0]  # HHMM
mode = None  # None, 'A', 'B'
display_on = True
error_led = False
pm_indicator = False
global toggle_display
global ssd_values
global p_m  
global digit_count, num1, num2, num3, num4, input_mode, A_mode, B_mode, manual_time, p_m

# Utility Functions

def invalid():
    GPIO.output(led_pin, GPIO.HIGH)

# Timing method
def pause(duration):
    start_uptime = readSystemUptime()
    current_uptime = start_uptime
    while(current_uptime != start_uptime + duration):
        current_uptime = readSystemUptime()
        detectKeyPress()

def readSystemUptime():
    with open("/proc/uptime", "r") as uptime_file:
        system_uptime = uptime_file.read().split(" ")[0].strip()
        return int(float(system_uptime))

def pulse_clock(ssd):
    GPIO.output(clock_pins[ssd - 1], GPIO.HIGH)
    GPIO.output(clock_pins[ssd - 1], GPIO.LOW)

def display_number(number, ssd, toggle_last_index=False):
    # Define the segment configurations for each digit (0-9)
    # Note: These configurations might need to be adjusted for your specific hardware setup.
    digit_segments = {
        0: [1, 1, 1, 1, 1, 1, 0, 0],  # 0
        1: [0, 1, 1, 0, 0, 0, 0, 0],  # 1
        2: [1, 1, 0, 1, 1, 0, 1, 0],  # 2
        3: [1, 1, 1, 1, 0, 0, 1, 0],  # 3
        4: [0, 1, 1, 0, 0, 1, 1, 0],  # 4
        5: [1, 0, 1, 1, 0, 1, 1, 0],  # 5
        6: [1, 0, 1, 1, 1, 1, 1, 0],  # 6
        7: [1, 1, 1, 0, 0, 0, 0, 0],  # 7
        8: [1, 1, 1, 1, 1, 1, 1, 0],  # 8
        9: [1, 1, 1, 1, 0, 1, 1, 0],  # 9
    }

    # Retrieve the segment configuration for the given number
    segments = digit_segments.get(number, [0, 0, 0, 0, 0, 0, 0, 0])

    # Toggle the last segment if requested
    if toggle_last_index:
        segments[-1] = 1 - segments[-1]

    # Set the state of each segment pin
    for pin, state in zip(data_pins, segments):
        GPIO.output(pin, state)

    # Pulse the clock to display the number on the specified SSD
    pulse_clock(ssd)


def reset_display():
    for pin in data_pins:
        GPIO.output(pin, GPIO.LOW)
    for ssd in range(1, 5):
        pulse_clock(ssd)

def restart_display():
    for i in range(1, 5):
        display_number(0, i)

def get_initial_time():
    now = datetime.now()
    return now.strftime("%H%M")

# Main Functionality
def handle_hash_key():
    # Implement hash key functionality
    

    # Toggle the display state
    toggle_display = not toggle_display

    if toggle_display:
        for ssd, number in enumerate(ssd_values, start=1):
            display_number(number, ssd, toggle_last_index=(ssd == 3 and p_m))
        time.sleep(0.5)  # Adjust the delay as needed
    else:
        # If the display is to be turned off, clear all segments
        for ssd in range(1, 5):
            display_number(0, ssd)  
        time.sleep(0.5)  # Adjust the delay as needed

def handle_a_key():
    # Implement 'A' key functionality
    def handle_a_key():
        global A_mode, time_values, p_m
        A_mode = not A_mode  # Toggle the A_mode

    if A_mode:
        print("Automatic mode activated")
        while A_mode:
            current_time = datetime.now()
            time_values[0] = current_time.hour // 10
            time_values[1] = current_time.hour % 10
            time_values[2] = current_time.minute // 10
            time_values[3] = current_time.minute % 10

            # Handle AM/PM logic if you are using 12-hour format
            if current_time.hour >= 12:
                p_m = True
            else:
                p_m = False

            # Display the time
            for index, value in enumerate(time_values):
                display_number(value, 4 - index)

            # Wait for a minute before updating time again
            time.sleep(60)
    else:
        print("Automatic mode deactivated")


def handle_b_key():

    if not B_mode:
        # Enter manual mode if 'B' is pressed and not already in B_mode
        B_mode = True
        input_mode = True
        digit_count = 0
        print("Enter manual time setting mode:")
    else:
        # Increment b_count if already in B_mode
        b_count += 1

        # If 'B' is pressed three times, reset and exit B_mode
        if b_count >= 3:
            print("Exiting manual time setting mode.")
            B_mode = False
            input_mode = False
            b_count = 0
            digit_count = 0
            # Reset the time values
            num1, num2, num3, num4 = 0, 0, 0, 0
            restart()  # Function to reset the display


def handle_digit_key(value):

    # If we are not in input mode, ignore digit keys
    if not input_mode:
        return

    # Convert value to integer
    num = int(value)
    digit_count += 1

    # Assign the digit to the correct position
    if digit_count == 1:
        num1 = num
        display_number(num1, 4)
    elif digit_count == 2:
        num2 = num
        display_number(num2, 3)
    elif digit_count == 3:
        num3 = num
        display_number(num3, 2)
    elif digit_count == 4:
        num4 = num
        display_number(num4, 1)

        # After all digits are entered, store the time
        manual_time = [num1, num2, num3, num4]
        print("Manual time set to: {}{}:{}{}".format(num1, num2, num3, num4))

        # Check if the entered time is in PM and adjust the `p_m` flag accordingly
        if num1 == 1 and num2 > 2:
            p_m = True
        elif num1 == 2:
            p_m = True if num2 in [0, 1, 2, 3] else False  # Assuming 24h format, 20-23 is PM
        else:
            p_m = False

        # Exit input mode
        input_mode = False
        B_mode = True  # If you want to start the time increment from here

        # Reset digit count
        digit_count = 0


def key_press():
    value = keypad_reader.read_key()
    if value is not None:
        if value == "#":
            handle_hash_key()
        elif value == "A":
            handle_a_key()
        elif value == "B":
            handle_b_key()
        elif value.isdigit():
            handle_digit_key(value)

def autoClock():
    GPIO.output([Clk1, Clk2, Clk3, Clk4], GPIO.LOW)  # Set clock displays to LOW
    now = datetime.now()
    
    # Convert hour to 12-hour format and use dot indicator for AM/PM
    hour = now.hour % 12 or 12  # Adjusts 0 hour to 12 for 12-hour format
    useDot() if hour in [12, 0] else None

    # Format hour and minute to 2-digit strings
    hour, minute = f"{hour:02d}", f"{now.minute:02d}"

    return hour, minute
   
def runAutoClock():
    global interrupt
    interrupt = False
    hourDigit, minuteDigit = autoClock()
    
    # Update displays with individual digits
    for i, digit in enumerate(hourDigit + minuteDigit):
        loadDisplay([Clk1, Clk2, Clk3, Clk4][i], digit)
        last[i] = digit
    
    while not interrupt:
        manualTimer()
        if interrupt: break
        increment()

def manual_time():

    while B_mode:
        wait(60)  # Pause for 60 seconds


        # Increment the minutes' least significant digit
        if manual_time[3] < 9:
            manual_time[3] += 1
        else:
            manual_time[3] = 0
            # Increment the tens-of-minutes
            if manual_time[2] < 5:
                manual_time[2] += 1
            else:
                manual_time[2] = 0
                # Increment the hours
                if manual_time[1] < 9:
                    manual_time[1] += 1
                else:
                    manual_time[1] = 0
                    if manual_time[0] < 2:
                        manual_time[0] += 1
                    elif manual_time[0] == 2:
                        manual_time[0] = 0
                        # Handle PM to AM transition
                        p_m = not p_m
                        if not p_m and manual_time[0] == 0 and manual_time[1] == 0:
                            # Reset to AM
                            p_m = False

        print(manual_time)

        # Update display with or without PM indicator
        if p_m:
            # PM: activate the PM dot indicator for the hour's tens place
            display_number(manual_time[3], 1)
            display_number(manual_time[2], 2)
            display_number(manual_time[1], 3, toggle_last_index=True)  # Toggle for PM
            display_number(manual_time[0], 4)
        else:
            # AM: display normally without toggling the last index
            display_number(manual_time[3], 1)
            display_number(manual_time[2], 2)
            display_number(manual_time[1], 3)
            display_number(manual_time[0], 4)

def runManualClock():
    global interrupt
    interrupt = False
    while not interrupt:
        time.sleep(0.1)
        manualValue = read_keypad()
        if manualValue:
            processManualInput(manualValue) 
        else:
            flashUnselectedPositions()  

def main():
    try:
        initial_time = get_initial_time()
        reset_display()
        restart_display()
        while True:
            key_press()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
