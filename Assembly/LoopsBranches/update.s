@mmap part taken from by https://bob.cs.sonoma.edu/IntroCompOrg-RPi/sec-gpio-mem

@ Constants for GPIO22
@ GPFSEL2 [Offset: 0x08] responsible for GPIO Pins 20 to 29
@ GPCLR0 [Offset: 0x28] responsible for GPIO Pins 0 to 31
@ GPSET0 [Offest: 0x1C] responsible for GPIO Pins 0 to 31

@ GPIO22 Related
.equ    GPFSEL2, 0x08   @ function register offset
.equ    GPCLR0, 0x28    @ clear register offset
.equ    GPSET0, 0x1c    @ set register offset
.equ    GPFSEL2_GPIO22_MASK, 0b111000000   @ Mask for fn register
.equ    MAKE_GPIO22_OUTPUT, 0b1000000      @ use pin for output
.equ    PIN, 22                         @ Used to set PIN high / low

@ Args for mmap
.equ    OFFSET_FILE_DESCRP, 0   @ file descriptor
.equ    mem_fd_open, 3
.equ    BLOCK_SIZE, 4096        @ Raspbian memory page
.equ    ADDRESS_ARG, 3          @ device address

@ Misc
.equ    SLEEP_IN_S, 1            @ sleep one second

@ The following are defined in /usr/include/asm-generic/mman-common.h:
.equ    MAP_SHARED, 1    @ share changes with other processes
.equ    PROT_RDWR, 0x3   @ PROT_READ(0x1)|PROT_WRITE(0x2)

@ Constant program data
.section .rodata
device:
    .asciz  "/dev/gpiomem"

@ The program
    .text
    .global main
main:
@ Open /dev/gpiomem for read/write and syncing
    ldr     r1, O_RDWR_O_SYNC   @ flags for accessing device
    ldr     r0, mem_fd          @ address of /dev/gpiomem
    bl      open
    mov     r4, r0              @ use r4 for file descriptor

@ Map the GPIO registers to a main memory location so we can access them
@ mmap(addr[r0], length[r1], protection[r2], flags[r3], fd[r4])
    str     r4, [sp, #OFFSET_FILE_DESCRP]   @ r4=/dev/gpiomem file descriptor
    mov     r1, #BLOCK_SIZE                 @ r1=get 1 page of memory
    mov     r2, #PROT_RDWR                  @ r2=read/write this memory
    mov     r3, #MAP_SHARED                 @ r3=share with other processes
    mov     r0, #mem_fd_open                @ address of /dev/gpiomem
    ldr     r0, GPIO_BASE                   @ address of GPIO
    str     r0, [sp, #ADDRESS_ARG]          @ r0=location of GPIO
    bl      mmap
    mov     r5, r0           @ save the virtual memory address in r5

@ Set up the GPIO pin function register in programming memory
    add     r0, r5, #GPFSEL2            @ calculate address for GPFSEL2
    ldr     r2, [r0]                    @ get entire GPFSEL2 register
    bic     r2, r2, #GPFSEL2_GPIO22_MASK @ clear pin field
    orr     r2, r2, #MAKE_GPIO22_OUTPUT  @ enter function code for GPIO22
    str     r2, [r0]                    @ update register

@ Give the value of the On_time and Off_time (On: 1sec, Off: 1sec=total:2sec)
@.equ On_time,     1000000000
@.equ Off_time,    1000000000

@ Give the value of the On_time and Off_time (1HZ: (50/50)dutycycles)
@.equ On_time,     450000000
@.equ Off_time,    450000000

@100 Hz 50/50
@.equ On_time,     4500000
@.equ Off_time,    4500000

@ Give the value of the On_time and Off_time (1kHZ: (25/75)dutycycles)
.equ On_time,     225000
.equ Off_time,    675000

@ Give the value of the On_time and Off_time (1kHZ: (50/50)dutycycles)
@.equ On_time,     450000
@.equ Off_time,    450000

@ Give the value of "fastest can run a square wave" the On_time and Off_time
@.equ On_time,     4500
@.equ Off_time,    4500



@ Loop to turn on and off GPIO22
loop:
@ Turn on
    add     r0, r5, #GPSET0     @ calc GPSET0 address
    mov     r3, #1              @ reset the r2 blink value
    lsl     r3, r3, #PIN        @ shift bit to pin position
    orr     r2, r2, r3          @ set bit
    str     r2, [r0]            @ update register
    ldr     r6, = On_time       @ load On_time into r6

@ Delay for On_time
delay_On_time:    
    subs     r6, r6, #1             @ Decrement the delay counter r6 by 1
    bne      delay_On_time      @ If r6 is not zero (branch not equal), loop back to delay_On_time

@ Turn off
    mov     r1, #1
    add     r0, r5, #GPCLR0      @ calc GPCLR0 address
    mov     r3, #1               @ reset the r2 blink value
    lsl     r3, r3, #PIN         @ shift bit to pin position
    orr     r2, r2, r3           @ set bit
    str     r2, [r0]             @ update register
    ldr     r8, =Off_time        @ load Off_time into r8

@ Delay for Off_time
delay_Off_time:
    subs     r8, r8, #1          @ Decrement the delay counter r8 by 1
    bne      delay_Off_time      @ If r8 is not zero (branch not equal), loop back to delay_Off_time

b loop

GPIO_BASE:
    .word   0xfe200000  @ GPIO Base address Raspberry pi 4
mem_fd:
    .word   device
O_RDWR_O_SYNC:
    .word   2|256       @ O_RDWR (2)|O_SYNC (256).
