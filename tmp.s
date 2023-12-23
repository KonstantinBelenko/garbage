.global _main
terminate_program:
mov x0, #0
mov x16, #1
svc 0
.data
.align 3
literal_0: .asciz "hello world"
.text
_main:
adrp x0, literal_0@PAGE
add x0, x0, literal_0@PAGEOFF
b terminate_program