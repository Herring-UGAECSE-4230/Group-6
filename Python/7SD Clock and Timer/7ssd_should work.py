# Imports for file
import time
import RPi.GPIO as GPIO



# Defining GPIO mode and input/output
GPIO.setmode(GPIO.BCM)

# X-Values (Horizontal) Mapping
GPIO.setup(18, GPIO.OUT) 
GPIO.setup(23, GPIO.OUT) 
GPIO.setup(24, GPIO.OUT) 
GPIO.setup(25, GPIO.OUT) 

# Y-Values (Vertical) Mapping
GPIO.setup(12, GPIO.IN) 
GPIO.setup(16, GPIO.IN) 
GPIO.setup(20, GPIO.IN) 
GPIO.setup(21, GPIO.IN) 

# Clock Setup
Clk1 = 26
Clk2 = 10
Clk3 = 9
Clk4 = 11

# Seven Segment Setup
DP = 19
A = 17
B = 4
C = 5
D = 6
E = 13
F = 27
G = 22
LED = 12

GPIO.setup(Clk1, GPIO.OUT) # Clock 1
GPIO.setup(Clk2, GPIO.OUT) # Clock 2
GPIO.setup(Clk3, GPIO.OUT) # Clock 3
GPIO.setup(Clk4, GPIO.OUT) # Clock 4

GPIO.setup(E, GPIO.OUT) # E
GPIO.setup(D, GPIO.OUT) # D
GPIO.setup(C, GPIO.OUT) # C
GPIO.setup(DP, GPIO.OUT) # DP
GPIO.setup(G, GPIO.OUT) # G
GPIO.setup(F, GPIO.OUT) # F
GPIO.setup(A, GPIO.OUT) # A
GPIO.setup(B, GPIO.OUT) # B
GPIO.setup(LED, GPIO.OUT) #LED gpio

count = 0
enable = True
last1 = []
last2 = []
last3 = []
last4 = []

# Resets SSD Display
def resetGPIO(Clk):
    GPIO.output(Clk, GPIO.HIGH)
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
    GPIO.output(Clk, GPIO.LOW)
    
def loadLast(Clk, *last):
    GPIO.output(*last, GPIO.HIGH)
    GPIO.output(Clk, GPIO.HIGH)
    GPIO.output(*last, GPIO.LOW)
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
    GPIO.output([Clk1,Clk2,Clk3,Clk4], GPIO.LOW)
    
    # Clock 1 will be used for row 1
    row1 = readKeypad(18,[1,2,3,'A'])
    if row1 == 1 and enable:
        resetGPIO(Clk1)
        last1 = [B,C]
        GPIO.output([B,C], GPIO.HIGH)
        GPIO.output(Clk1, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk1, GPIO.LOW)
        
    elif row1 == 2 and enable:
        resetGPIO(Clk1)
        last1 = [A,B,G,E,D]
        GPIO.output([A,B,G,E,D], GPIO.HIGH)
        GPIO.output(Clk1, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk1, GPIO.LOW)
    elif row1 == 3 and enable:
        resetGPIO(Clk1)
        last1 = [A,B,C,G,D]
        GPIO.output([A,B,C,G,D], GPIO.HIGH)
        GPIO.output(Clk1, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk1, GPIO.LOW)
    elif row1 == 'A' and enable:
        resetGPIO(Clk1)
        last1 = [F, A, E, B, C, G]
        GPIO.output([F, A, E, B, C, G], GPIO.HIGH)
        GPIO.output(Clk1, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk1, GPIO.LOW)
        
        
    # Clock 2 will be used for row 2
    row2 = readKeypad(23,[4,5,6,'B'])
    if row2 == 4 and enable:
        resetGPIO(Clk2)
        last2 = [F, G, B, C]
        GPIO.output([F, G, B, C], GPIO.HIGH)
        GPIO.output(Clk2, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk2, GPIO.LOW)
    elif row2 == 5 and enable:
        resetGPIO(Clk2)
        last2 = [A, F, G, C, D]
        GPIO.output([A, F, G, C, D], GPIO.HIGH)
        GPIO.output(Clk2, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk2, GPIO.LOW)
    elif row2 == 6 and enable:
        resetGPIO(Clk2)
        last2 = [A,F,G,C,D,E]
        GPIO.output([A,F,G,C,D,E], GPIO.HIGH)
        GPIO.output(Clk2, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk2, GPIO.LOW)
    elif row2 == 'B' and enable:
        resetGPIO(Clk2)
        last2 = [F,E,D,C,G]
        GPIO.output([F,E,D,C,G], GPIO.HIGH)
        GPIO.output(Clk2, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk2, GPIO.LOW)

    # Clock 3 will be used for row 3
    row3 = readKeypad(24,[7,8,9,'C'])
    if row3 == 7 and enable:
        resetGPIO(Clk3)
        last3 = [A,B,C]
        GPIO.output([A,B,C], GPIO.HIGH)
        GPIO.output(Clk3, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk3, GPIO.LOW)
    elif row3 == 8 and enable:
        resetGPIO(Clk3)
        last3 = [A,B,C,D,E,F,G]
        GPIO.output([A,B,C,D,E,F,G], GPIO.HIGH)
        GPIO.output(Clk3, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk3, GPIO.LOW)
    elif row3 == 9 and enable:
        resetGPIO(Clk3)
        last3 = [A,B,C,F,G]
        GPIO.output([A,B,C,F,G], GPIO.HIGH)
        GPIO.output(Clk3, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk3, GPIO.LOW)
    elif row3 == 'C' and enable:
        resetGPIO(Clk3)
        last3 = [A,F,E,D]
        GPIO.output([A,F,E,D], GPIO.HIGH)
        GPIO.output(Clk3, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk3, GPIO.LOW)
        
    #Clock 4 will be used for row 4
    row4 = readKeypad(25,['*',0,'#','D'])
    if row4 == '*' and enable:
        resetGPIO(Clk4)
        last4 = [DP]
        GPIO.output([DP], GPIO.HIGH)
        GPIO.output(Clk4, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk4, GPIO.LOW)
    elif row4 == 0 and enable:
        resetGPIO(Clk4)
        last4 = [A,B,F,C,E,D]
        GPIO.output([A,B,F,C,E,D], GPIO.HIGH)
        GPIO.output(Clk4, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk4, GPIO.LOW)
    elif row4 == '#':
        resetGPIO(Clk4)
        print("display")
        if(enable):
                GPIO.output([Clk1,Clk2, Clk3, Clk4], GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output([Clk1,Clk2, Clk3, Clk4], GPIO.LOW)
                enable = False
                time.sleep(.1)
                print(enable)
        else: 
               enable = True
               loadLast(Clk1,last1)
               loadLast(Clk2,last2)
               loadLast(Clk3,last3)
               loadLast(Clk4,last4)
               print(enable)
            
    elif row4 == 'D' and enable:
        resetGPIO(Clk4)
        if (count % 2 == 0):
            count = count +1
            GPIO.output(LED, GPIO.HIGH)
            time.sleep(.2)
        else:
            count = count +1
            GPIO.output(LED, GPIO.LOW)
            time.sleep(.2)

        time.sleep(0.1)
        GPIO.output(Clk4, GPIO.LOW)
   
    
    GPIO.output([Clk1,Clk2,Clk3,Clk4], GPIO.LOW)