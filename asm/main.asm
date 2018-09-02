; @file main.asm
; @author sb
; @brief testing mode for assembly language programming


section .text
global _start									; let the assembler know the start of the program

_start:
	mov edx, len								; length of the message
	mov ecx, msg								; message to be written
	mov ebx, 1									; provide the file descriptor(stdout in this case)
	mov eax, 4									; system call number(sys_write)
	int 80h											; interrupt and call the kernel

	mov eax, 1									; system call number(sys_exit)
	int 80h											; interrupt and call the kernel

section .data
msg db 'Working!', 0ah				; string to be printed
len equ $ - msg 							; length of the message
