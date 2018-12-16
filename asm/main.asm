; @file main.asm
; @author sb
; @brief testing mode for assembly language programming

section .data
EXIT_SUCCESS equ 0					; successful operation
EXIT_FAILURE equ 1					; erroneous operation
SYS_EXIT equ 60							; call code to terminate

; 8 bit variable space (byte)
bVar1 db 17
bVar2 db 9
bResult db 0

; 16 bit variable space (word)
wVar1 dw 17000
wVar2 dw 9000
wResult dw 0

; 32 bit variable space (double word)
dVar1 dd 17000000
dVar2 dd 9000000
dResult dd 0

; 64 bit variable space (quad word)
qVar1 dq 170000000
qVar2 dq 90000000
qResult dq 0

; code section
section .text
global _start

_start:
	; 8 bit addition
	mov al, byte [bVar1]
	add al, byte [bVar2]
	mov byte [bResult], al

	; 16 bit addition
	mov ax, word [wVar1]
	add ax, word [wVar2]
	mov word [wResult], ax

	; 32 bit addition
	mov eax, dword [dVar1]
	add eax, dword [dVar2]
	mov dword[dResult], eax

	; 64 bit addition
	mov rax, qword [qVar1]
	add rax, qword [qVar2]
	mov qword [qResult], rax

; return code for the execution of the program
last:
	mov rax, SYS_EXIT					; call code for exit
	mov rdi, EXIT_SUCCESS 		; exit the program with success
	syscall
