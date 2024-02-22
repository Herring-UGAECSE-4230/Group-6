import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)
from time import sleep

X1 = 18
X2 = 23
X3 = 24
X4 = 25
Y1 = 12
Y2 = 16
Y3 = 20
Y4 = 21

e = 4
d = 17
c = 27
dot = 22
b = 5
a = 6
f = 13
g = 19
invalid = 8

clk1 = 10
clk2 = 9
clk3 = 7
clk4 = 26
clk5 = 11

counter = 0
number = 0

toggle = False
clear = False
set1 = False
set2 = False
set3 = False
set4 = False

clock = [clk1,clk2,clk3,clk4]
dff_pins = [a,b,c,d,e,f,g]

GPIO.setup([X1,X2,X3,X4, dot, invalid], GPIO.OUT)
GPIO.setup([Y1,Y2,Y3,Y4], GPIO.IN)
GPIO.setup(dff_pins, GPIO.OUT)
GPIO.setup([clk1,clk2,clk3, clk4,clk5], GPIO.OUT)

def readKeypad(rowNum,char):
    if clear == False:
        curVal = ""
        GPIO.output(rowNum,GPIO.HIGH)
        if GPIO.input(Y1)==1: curVal=char[0]
        if GPIO.input(Y2)==1: curVal=char[1]
        if GPIO.input(Y3)==1: curVal=char[2]
        if GPIO.input(Y4)==1: curVal=char[3]
        GPIO.output(rowNum,GPIO.LOW)
        return curVal
    if clear == True:
        curVal = ""
        GPIO.output(rowNum, GPIO.HIGH)
        if GPIO.input(Y3) == 1:
            curVal = char[2]
        GPIO.output(rowNum,GPIO.LOW)
        return curVal
        

bin_vals = {0:[1,1,1,1,1,1,0], 
            1:[0,1,1,0,0,0,0], 
            2:[1,1,0,1,1,0,1], 
            3:[1,1,1,1,0,0,1], 
            4:[0,1,1,0,0,1,1], 
            5:[1,0,1,1,0,1,1], 
            6:[1,0,1,1,1,1,1], 
            7:[1,1,1,0,0,0,0], 
            8:[1,1,1,1,1,1,1], 
            9:[1,1,1,1,0,1,1],            
            'A':[1,1,1,0,1,1,1], 
            'B':[0,0,1,1,1,1,1], 
            'C':[0,0,0,1,1,0,1], 
            'D':[0,1,1,1,1,0,1], 
            }

def output(gpio_list, states):
    for i in range(len(gpio_list)):
        GPIO.output(gpio_list[i], states[i])
       
def switch(gpio):
    global clear,last, dots
    clear = not clear
    if clear == True:
        last = [GPIO.input(i) for i in dff_pins]
        dots = GPIO.input(dot)
        output(gpio,[0,0,0,0,0,0,0])
        if GPIO.input(dot) == 1:
            GPIO.output(dot,0)
            
    if clear == False:
        output(gpio, last)
#         if dots == 1:
#             GPIO.output(dot,1)
#         if dots == 0:
#             GPIO.output(dot,0)
            
def ssd_disp(clk_num, value):
    global clock, setssd, counter, number, toggle
    
    try:
        
        value = int(value)
        output(dff_pins, bin_vals[value])
        GPIO.output(invalid, 0)
        counter += 1
        number += 1
        
    except:
        if value == 'A':
            GPIO.output(invalid, 1)
            
        if value == 'B':
            GPIO.output(invalid, 1)
            
        if value == 'C':
            GPIO.output(invalid, 1)
            
        if value == 'D':
            GPIO.output(invalid, 1)
            
        if value == '*':
            if GPIO.input(dot) == 0: GPIO.output(dot, 1)
            else: GPIO.output(dot, 0)
        if value == '#':
            #switch(dff_pins)
            toggle = not toggle
            
def latch_value(clk_num):
    GPIO.output(clk_num, 1)
    sleep(0.05)
    GPIO.output(clk_num, 0)
    sleep(0.05)

def ssdLoop(clk_num):
    global counter
    if clear == False:
        ssd_disp(clk_num, readKeypad(X1, [1,2,3,'A']))
        ssd_disp(clk_num, readKeypad(X2, [4,5,6,'B']))
        ssd_disp(clk_num, readKeypad(X3, [7,8,9,'C']))
        ssd_disp(clk_num, readKeypad(X4, ['*',0,'#','D']))
        latch_value(clk_num)
        sleep(.1)
        
    if clear == True:
        ssd_disp(clk_num, readKeypad(X4, ['*',0,'#','D']))
        latch_value(clk_num)
        sleep(.1)
     

output(dff_pins, [1,1,1,1,1,1,1,1])

try:
    while True:  
        while counter != 4:
            switch(dff_pins) #this makes each SSD flash until a value is input
            if counter == 0:
                ssdLoop(clk1)
                sleep(.2)
                last1 = [GPIO.input(i) for i in dff_pins]
                pin1 = dff_pins
            if counter == 1:
                ssdLoop(clk2)
                sleep(.2)
                last2 = [GPIO.input(i) for i in dff_pins]
                pin2 = dff_pins
            if counter == 2:
                ssdLoop(clk3)
                sleep(.2)
                pin3 = dff_pins
                last3 = [GPIO.input(i) for i in dff_pins]
            if counter == 3:
                ssdLoop(clk4)
                sleep(.2)
                pin4 = dff_pins
                last4 = [GPIO.input(i) for i in dff_pins]
        
        while counter >= 4:
            last_dff = [last1,last2,last3,last4]
            pin_dff = [pin1,pin2,pin3,pin4]
            ssdLoop(clk5) 
            if toggle == False:
                for x in range(4):
                    print(x)
                    output(pin_dff[x], last_dff[x])
                    ssdLoop(clock[x])
            if toggle == True:
                for x in range(4):
                    output(pin_dff[x], [0,0,0,0,0,0,0,0])
                    ssdLoop(clock[x])
                
                
except KeyboardInterrupt: 
    GPIO.cleanup()

# ssdLoop(clk1)
# ssdLoop(clk2)
# ssdLoop(clk3)
# ssdLoop(clk4)