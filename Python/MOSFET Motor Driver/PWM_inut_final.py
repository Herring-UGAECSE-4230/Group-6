import RPi.GPIO as GPIO
import time

# GPIO Pin setup
clk = 26
dt = 19
sw = 13

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize variables
counter = 0
clkLastState = GPIO.input(clk)
swLastState = GPIO.input(sw)

# Improved Debounce Method
def debounce(pin):
    debounce_time = 0.02
    current_state = GPIO.input(pin)
    time.sleep(debounce_time)
    if GPIO.input(pin) == current_state:
        return True
    else:
        return False

# Main loop
try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        swState = GPIO.input(sw)
        
        # Only check for button press if state has changed and debounce confirms
        if swState != swLastState and debounce(sw):
            if swState == False:
                print("Button Pressed")
                time.sleep(0.1)  # Additional debounce/wait time after a press is detected
        
        if clkState != clkLastState and debounce(clk):
            if dtState != clkState:
                counter += 1
                direction = "Clockwise"
            else:
                counter -= 1
                direction = "Counter-Clockwise"
            print("Direction:", direction, "Counter:", counter)
        
        clkLastState = clkState
        swLastState = swState

        time.sleep(0.01)  # Loop delay for debouncing

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
