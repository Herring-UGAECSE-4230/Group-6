@ Deliverable 1: Describe how the stmdb instruction works in myFunc.
@ Deliverable 2: Describe how the ldmia instruction works in myFunc.
@ Deliverable 3: What is the value of R0, R1, and R2 after the program runs?
@ Deliverable 4: Replace the stmdb and ldmia instructions in myFunc with the appropriate (least number) of push and pop instructions.  Show your code.


	.text
	.global _start
_start: ldr  	r0, =0x125	@ r0 = 0x125
	ldr  	r1, =0x144	@ r1 = 0x144
	mov  	r2, #0x56	@ r2 = 0x56
	bl	myFunc		@ call a subroutine
	add	r3, r0, r1	@ r3 = r0 + r1 = 0x125 + 0x144 = 0x269
	add	r3, r3, r2	@ r3 = r3 + r2 = 0x269 + 0x56 = 0x2bf
	mov	r7, #1
	svc	0
	@ ---------------------------

myFunc:
	@ push registers onto the stack	
	push   {r0, r1, r2}

	@ --------r0, r1, and r2 are changed
	mov  	r0, #0	 	@ r0=0
	mov  	r1, #0	 	@ r1=0
	mov  	r2, #0	 	@ r2=0

	@ Pop original registers contents from stack
	pop		{r2, r1, r0}

	bx	lr 		@ return to caller
