from shared_utils import verify_codegen

def test():
    print("Running codegen math test...")
    
    verify_codegen('2 + 2;', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    literal_0: .word 2',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Numeric Literal')
    
    verify_codegen('2 + 4;', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    literal_0: .word 2',
        '    literal_1: .word 4',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Two numeric literals')
    
    verify_codegen('2 + 4;', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    literal_0: .word 6',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Two numeric literals optimized', optimize=True)
    
    verify_codegen("(2 + 2) * 2;", [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    literal_0: .word 8',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Parentheses optimized', optimize=True)