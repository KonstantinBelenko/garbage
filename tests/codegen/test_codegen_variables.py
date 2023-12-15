from shared_utils import verify_codegen

def test():
    print("Running codegen variables test...")
    
    verify_codegen('let x = 42;', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    x: .word 42',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Static Numeric Literal Assignment', optimize=True)
    
    verify_codegen('let x = 5 + 5 * 4;', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    x: .word 25',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Static Numeric Expression Assignment', optimize=True)
    
    verify_codegen('''
        let x = 42;
        let y = 42;
        let c = x + y;
    ''', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    x: .word 42',
        '    y: .word 42',
        '    c: .word 0',
        '',
        '.text',
        '_main:',
        '    adrp x1, x@PAGE',
        '    add x1, x1, x@PAGEOFF',
        '    ldr w2, [x1]',
        '    adrp x3, y@PAGE',
        '    add x3, x3, y@PAGEOFF',
        '    ldr w4, [x3]',
        '    add w2, w2, w4',
        '    adrp x5, c@PAGE',
        '    add x5, x5, c@PAGEOFF',
        '    str w2, [x5]',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Dynamic Variable Assignment', optimize=True)
    
    verify_codegen('''
        let x = 3;
        let y = 2;
        let c = y * (x + 2);
    ''', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    x: .word 3',
        '    y: .word 2',
        '    c: .word 0',
        '',
        '.text',
        '_main:',
        '    adrp x1, x@PAGE',
        '    add x1, x1, x@PAGEOFF',
        '    ldr w2, [x1]',
        '    adrp x3, y@PAGE',
        '    add x3, x3, y@PAGEOFF',
        '    ldr w4, [x3]',
        '    add w5, w2, #2',
        '    mul w2, w4, w5',
        '    adrp x5, c@PAGE',
        '    add x5, x5, c@PAGEOFF',
        '    str w2, [x5]',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Multi varible expression assignment', optimize=True)