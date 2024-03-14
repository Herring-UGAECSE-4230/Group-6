import RPi.GPIO as GPIO
import time

#GPIO Setup
GPIO.setmode(GPIO.BCM)
clk =22
dt = 27
sw = 17
GPIO.setup([clk,dt,sw], GPIO.IN)

#Allowing for dt and clk to have an internal pull up
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#start time to track turns per second
start = time.time()
previousFreq = 0
tps = 0

#deobounce method
def debounce(input):
 global start, previousFreq, tps
    
  # Calculate difference in time between start and currewnt time
 now = time.time()
 difference = abs(now - start)
    
  # shows change from last signal to help filter random noise
 change = abs(input - previousFreq)
    
  # essentially creates a threshold to filter out some noise we encountered
 if abs(change) > .2:
      
    tps = change / difference
    print("Turns per second: ", tps)
    # Update tps based on change of freqeuncy and difference in time
    # Update previous values 
    start = now
    previousFreq = input
    
   #time.sleep for time based debounce
 time.sleep(.01)
    

#defining last state and intializing the counter
counter=0
lastClkState=GPIO.input(clk)
lastswState=GPIO.input(sw)


#main loop to monitor encoder
while True:
  
  direction = "none"
  #monitors gpio states
  clkState=GPIO.input(clk)
  dtState=GPIO.input(dt)
  swState=GPIO.input(sw)
  debounce(clkState)
  #the condionals to monitor the states of clk dt and sw 
  if swState!=lastswState:
    if swState == False:
      print("Press")
      time.sleep(0.1)
  if clkState!=lastClkState:
    if dtState!=clkState:
      counter+=1
      direction = "Clockwise"
    else:
      counter-=1
      direction = "CounterClockwise"
    lastClkState=clkState
  
 
  print("Direction: ", direction,"Counter: ", counter)
  