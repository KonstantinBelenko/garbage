.global _main
print_string:
ldrb w2, [x1]
cmp w2, #0
beq _print_string_end
mov x3, x1
mov x0, 1
mov x2, 1
mov x16, 4
svc 0
mov x1, x3
add x1, x1, #1
b print_string
_print_string_end:
ret
.data
.align 3
literal_0: .asciz "Hi!"
.text
_main:
adrp x1, literal_0@PAGE
add x1, x1, literal_0@PAGEOFF
bl print_string
mov x0, #0
mov x16, #1
svc 0