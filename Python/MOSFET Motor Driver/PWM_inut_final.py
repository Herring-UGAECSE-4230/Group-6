import RPi.GPIO as GPIO
import time

clk = 26
dt = 19
sw = 13

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initiate variables
counter = 0
direction = ""
last_clk_state = GPIO.input(clk)
last_sw_state = GPIO.input(sw)

# Debouncing Methods
def debounce(pin):
    debounce_time = 0.02 
    current_state = GPIO.input(pin)
    time.sleep(debounce_time)
    return GPIO.input(pin) == current_state


# Main Loop
try:
    while True:
        clk_state = debounce(clk)
        dt_state = debounce(dt)
        sw_state = debounce(sw)

        if sw_state != last_sw_state:
            if sw.state == False:
                print("Press")

        if clk_state != last_clk_state:
            if dt_state != clk_state:
                counter += 1
                direction = "Clockwise"
            else:
                counter -= 1
                direction = "Counter-Clockwise"

                
        print("Direction:", direction, "Counter:", counter)

        last_clk_state = clk_state
        last_sw_state = sw_state

        time.sleep(0.01)


except KeyboardInterrupt:
    GPIO.cleanup()
    