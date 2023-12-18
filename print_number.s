.global _main
.align 3

.data
x: .long 500

.text
_main:
    adrp x0, x@PAGE
    add x0, x0, x@PAGEOFF    

    bl convert_to_string

    mov x1, x0          // Set x1 to the address of the string
    ldr x2, =endstr     // Load address of end of string
    mov x2, #2      	// Calculate length of string
    mov x0, #1          // stdout
    mov x16, #4        	// syscall number for write
    svc 0

    mov x0, #0          // return 0 status
    mov x16, #1        // syscall number for exit
    svc 0

convert_to_string:
    ldr w1, [x0]        // Load the integer value
    mov x3, x0          // Save original address to x3
    add x2, x0, #10     // Temporarily set x2 to x0 + 10 as buffer end

    // Convert integer to string
    mov w3, #10         // w3 is the divisor for division by 10
    cbz w1, zero_case   // Special case for zero

conv_loop:
    udiv w4, w1, w3     // w4 = w1 / 10
    msub w5, w4, w3, w1 // w5 = w1 - (w4 * 10)
    add w5, w5, #48     // Convert to ASCII
    strb w5, [x2], #-1  // Store byte and pre-decrement address
    mov w1, w4          // Prepare next digit
    cbnz w1, conv_loop  // If w1 is not zero, continue loop
    b end_convert       // End conversion

zero_case:
    mov w5, #48         // ASCII for zero
    strb w5, [x2, #-1]  // Store '0'

end_convert:
    add x0, x2, #1      // Adjust x0 to point to the start of the string
    ret                 // Return

endstr: .byte 0        // Null-terminator for string
