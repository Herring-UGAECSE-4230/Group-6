# Arithmetic Operations in assembly
## Objective
This lab goes over the arithmetic operations in assembly and look into the debugger (GDB) and makefiles. The debugger is a great tool for walking through your program to understand what it is doing. The makefile can make recompiling a file multiple times much simpler. There are also many assembler flags that you can use.  The flag we will be looking at in this lab is the debug flag (-g). There is also a short write up about makefiles and the debugger you should read over and a couple of links so you can go more into detail.
Finally, we introduce the CPSR.  This may be one of the most important registers in the ARM processor.

## Instructions
1. Copy the folders and makefiles from this github directories
2. Use the terminal and the makefile to compile each of the .o files use the command "make DEBUG=1"
3. Run each program using gdb program name
4. Set a break point at the beginning of the files using b _start
5. run the program by typing run or r
6. step through each program and use the command i r to check the registers and see what is happening in the programs.

## Deliverables
1. For each program,show the output of the debugger with the final result including the CPSR.
2. Describe the CPSR.  What are bits 31, 30, 29, 28?
3. For the add and substract programs, change the ADD/SUB line only so that the result is zero.  Do not change the instruction.  What is the value of the Z-Flag?
4. For the add and substract programs, change the ADD/SUB line only so that you can see the Z bit set to 1 (CPSR). You may need to read about ADDS and SUBS.  Show your code and result of the CPSR.
5. What is the primary difference in the commands ADD vs ADDS and SUB vs SUBS?
6. For the SUB program what is the potential problem?  As inspiration, swap the SUB command to SUB R1, R0.  What should be the result?  What is the result?
