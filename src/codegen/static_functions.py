class StaticFunctions:
    
    @staticmethod
    def terminate_program() -> list[str]:
        return [
            'terminate_program:',
            'mov x0, #0',
            'mov x16, #1',
            'svc 0',
        ]
        
    @staticmethod
    def print_string() -> list[str]:
        return [
            'print_string:',
            'ldrb w2, [x1]',
            'cmp w2, #0',
            'beq _print_string_end',
            'mov x3, x1',
            'mov x0, 1',
            'mov x2, 1',
            'mov x16, 4',
            'svc 0',
            'mov x1, x3',
            'add x1, x1, #1',
            'b print_string',
            '_print_string_end:',
            'ret',
        ]
    
    @staticmethod
    def itoa() -> list[str]:
        return [
            'itoa:',
            'mov x2, x0',
            'mov x3, #0',
            'mov x4, #10',
            'mov x5, #0',
            '.itoa_count_loop:',
            'cmp x2, #0',
            'beq .itoa_count_end',
            'udiv x2, x2, x4',
            'add x3, x3, #1',
            'b .itoa_count_loop',
            '.itoa_count_end:',
            'mov x10, x3',
            'add x10, x10, #1',
            'sub sp, sp, x10',
            'mov x1, sp',
            'mov x2, x0',
            'mov x3, #0',
            'mov x4, #10',
            'mov x5, #0',
            'mov x6, #0',
            '.itoa_loop:',
            'udiv x6, x2, x4',
            'msub x3, x6, x4, x2',
            'add x3, x3, #48',
            'strb w3, [x1, x5]',
            'mov x2, x6',
            'add x5, x5, #1',
            'cmp x2, #0',
            'bne .itoa_loop',
            'mov x3, #10',
            'strb w3, [x1, x5]',
            'mov x7, #0',
            'sub x8, x5, #1',
            '.reverse_loop:',
            'cmp x7, x8',
            'bge .reverse_done',
            'ldrb w9, [x1, x7]',
            'ldrb w2, [x1, x8]',
            'strb w9, [x1, x8]',
            'strb w2, [x1, x7]',
            'add x7, x7, #1',
            'sub x8, x8, #1',
            'b .reverse_loop',
            '.reverse_done:',
            'mov x2, x10',
            'ret',
        ]

static_funcions = {
    'terminate_program': StaticFunctions.terminate_program,
    'print_string': StaticFunctions.print_string,
    'itoa': StaticFunctions.itoa,
}