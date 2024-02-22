#imports for file
import time
import RPi.GPIO as GPIO

#Definig GPIO mode and input/output
GPIO.setmode(GPIO.BCM)

# X-Values (Horizontal) Mapping
GPIO.setup(18, GPIO.OUT) #Yellow Wire X1
GPIO.setup(23, GPIO.OUT) #Orange Wire X2
GPIO.setup(24, GPIO.OUT) #Brown Wire X3
GPIO.setup(25, GPIO.OUT) #Red Wire X4

#  Y-Values (Vertical) Mapping
GPIO.setup(12, GPIO.IN) #Black Wire Y1
GPIO.setup(16, GPIO.IN) #White Wire Y2
GPIO.setup(20, GPIO.IN) #Gray Wire Y3
GPIO.setup(21, GPIO.IN) #Blue Wire Y4

#GPIO SETUP
Clk = 26
E = 13
D = 6
C = 5
DP = 19
G = 22
F = 27
A = 17
B = 4
GPIO.setup(Clk, GPIO.OUT) #Clock 1

GPIO.setup(E, GPIO.OUT) #E
GPIO.setup(D, GPIO.OUT) #D
GPIO.setup(C, GPIO.OUT) #C
GPIO.setup(DP, GPIO.OUT) #DP
GPIO.setup(G, GPIO.OUT) #G
GPIO.setup(F, GPIO.OUT) #F
GPIO.setup(A, GPIO.OUT) #A
GPIO.setup(B, GPIO.OUT) #B

display_on = True


    
# Resets SSD Display
def resetGPIO():
    GPIO.output(Clk, GPIO.HIGH)
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
    GPIO.output(Clk, GPIO.LOW)
    
# Conditional implementation of keypad
def readKeypad(rowNum, char):
  
    curVal = 0
    
    GPIO.output(rowNum, GPIO.HIGH)
    if GPIO.input(12) == 1:
        curVal = char[0]
        time.sleep(0.2)
        return curVal
        
    if GPIO.input(16) == 1:
        curVal = char[1]
        time.sleep(0.2)
        return curVal
        
    if GPIO.input(20) == 1:
        curVal = char[2]
        time.sleep(0.2)
        return curVal
        
    if GPIO.input(21) ==1:
        curVal = char[3]
        time.sleep(0.2)
        return curVal

    GPIO.output(rowNum, GPIO.LOW)

while True:

    GPIO.output(Clk, GPIO.LOW)

    
    row1 = readKeypad(18,[1,2,3,'A'])
    if row1 == 1:
        resetGPIO()
        GPIO.output([B,C], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)        
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row1 == 2:
        resetGPIO()
        GPIO.output([A,B,G,E,D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row1 == 3:
        resetGPIO()
        GPIO.output([A,B,C,G,D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row1 == 'A':
        resetGPIO()
        GPIO.output([F, A, E, B, C, G], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
        
    row2 = readKeypad(23,[4,5,6,'B'])
    if row2 == 4:
        resetGPIO()
        GPIO.output([F, G, B, C], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row2 == 5:
        resetGPIO()
        GPIO.output([A, F, G, C, D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row2 == 6:
        resetGPIO()
        GPIO.output([A,F,G,C,D,E], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row2 == 'B':
        resetGPIO()
        GPIO.output([F,E,D,C,G], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)

    row3 = readKeypad(24,[7,8,9,'C'])
    if row3 == 7:
        resetGPIO()
        GPIO.output([A,B,C], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row3 == 8:
        resetGPIO()
        GPIO.output([A,B,C,D,E,F,G], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row3 == 9:
        resetGPIO()
        GPIO.output([A,B,C,F,G], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row3 == 'C':
        resetGPIO()
        GPIO.output([A,F,E,D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)

    row4 = readKeypad(25,['*',0,'#','D'])
    if row4 == '*':
        resetGPIO()
        GPIO.output([DP], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row4 == 0:
        resetGPIO()
        GPIO.output([A,B,F,C,E,D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row4 == '#' and display_on is True:
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
        GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
        display_on = False
    elif row4 == '#' and display_on is False:
        resetGPIO()
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row4 == 'D':
        resetGPIO()
        GPIO.output([B,G,E,D,C], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    
    GPIO.output(Clk, GPIO.LOW)

