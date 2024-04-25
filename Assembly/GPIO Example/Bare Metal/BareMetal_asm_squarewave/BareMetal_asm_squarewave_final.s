.section .text
.globl _start

.equ GPIO_BASE, 0xFE200000
.equ GPFSEL2, 0x08
.equ GPIO_21_OUTPUT, 0x8
.equ GPFSET0, 0x1c
.equ GPFCLR0, 0x28
.equ GPIOVAL, 0x200000

.equ ON_TIME, 480000  // Define ON_TIME as 480000 nanoseconds
.equ OFF_TIME, 480000 // Define OFF_TIME as 480000 nanoseconds
// total 960000 nanoseconds for both ON and OFF times approximate a 1000Hz frequency

_start:
    // Initialize the program, starting point

    // Set GPIO pin 21 as output
    ldr r1, =GPIO_BASE       // Load the base address of the GPIO registers into r1
    ldr r2, =GPFSEL2         // Load the address of the GPIO Function Select Register 2 into r2
    ldr r3, =GPIO_21_OUTPUT  // Load the control value for setting GPIO 21 as output into r3
    str r3, [r1, r2]         // Store the control value in the GPFSEL2 register to set GPIO 21 as output

    // Loop forever
loop:
    // Turn on GPIO pin 21
    ldr r1, =GPIO_BASE    // Reload the base address of the GPIO registers into r1
    ldr r2, =GPFSET0      // Load the address of the GPIO Pin Output Set Register 0 into r2
    ldr r3, =GPIOVAL      // Load the value to set GPIO 21 into r3
    str r3, [r1, r2]      // Write to GPFSET0 to set GPIO 21 (turn it on)

    // Delay for ON_TIME nanoseconds
    ldr r4, =ON_TIME      // Load the ON_TIME value into r4
delay_on:
    subs r4, #1           // Subtract 1 from r4
    bne delay_on          // If r4 is not zero, branch back to delay_on (creating a delay)

    // Turn off GPIO pin 21
    ldr r1, =GPIO_BASE    // Reload the base address of the GPIO registers into r1
    ldr r2, =GPFCLR0      // Load the address of the GPIO Pin Output Clear Register 0 into r2
    ldr r3, =GPIOVAL      // Load the value to clear GPIO 21 into r3
    str r3, [r1, r2]      // Write to GPFCLR0 to clear GPIO 21 (turn it off)

    // Delay for OFF_TIME nanoseconds
    ldr r4, =OFF_TIME     // Load the OFF_TIME value into r4
delay_off:
    subs r4, #1           // Subtract 1 from r4
    bne delay_off         // If r4 is not zero, branch back to delay_off (creating a delay)

    // Repeat the loop
    b loop                // creating an infinite loop
