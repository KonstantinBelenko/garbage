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
        '    adrp x0, x@PAGE',
        '    add x0, x0, x@PAGEOFF',
        '    ldr w1, [x0]',
        '    adrp x2, y@PAGE',
        '    add x2, x2, y@PAGEOFF',
        '    ldr w3, [x2]',
        '    add w5, w1, w3',
        '    adrp x0, c@PAGE',
        '    add x0, x0, c@PAGEOFF',
        '    str w5, [x0]',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Dynamic Variable Assignment', optimize=True)
    
    verify_codegen('''
        let x = 42;
        let y = 42;
        let c = x + y + x;
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
        '    adrp x0, x@PAGE',
        '    add x0, x0, x@PAGEOFF',
        '    ldr w1, [x0]',
        '    adrp x2, y@PAGE',
        '    add x2, x2, y@PAGEOFF',
        '    ldr w3, [x2]',
        '    add w5, w1, w3',
        '    adrp x2, x@PAGE',
        '    add x2, x2, x@PAGEOFF',
        '    ldr w3, [x2]',
        '    add w5, w5, w3',
        '    adrp x0, c@PAGE',
        '    add x0, x0, c@PAGEOFF',
        '    str w5, [x0]',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Dynamic Variable Assignment with 2 variables 3 times chained.', optimize=True)
    
    verify_codegen('''
        let x = 2;
        let y = 3;
        let c = x + y;
        let d = c + x;
    ''', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    x: .word 2',
        '    y: .word 3',
        '    c: .word 0',
        '    d: .word 0',
        '',
        '.text',
        '_main:',
        '    adrp x0, x@PAGE',
        '    add x0, x0, x@PAGEOFF',
        '    ldr w1, [x0]',
        '    adrp x2, y@PAGE',
        '    add x2, x2, y@PAGEOFF',
        '    ldr w3, [x2]',
        '    add w5, w1, w3',
        '    adrp x0, c@PAGE',
        '    add x0, x0, c@PAGEOFF',
        '    str w5, [x0]',
        '    adrp x0, c@PAGE',
        '    add x0, x0, c@PAGEOFF',
        '    ldr w1, [x0]',
        '    adrp x2, x@PAGE',
        '    add x2, x2, x@PAGEOFF',
        '    ldr w3, [x2]',
        '    add w5, w1, w3',
        '    adrp x0, d@PAGE',
        '    add x0, x0, d@PAGEOFF',
        '    str w5, [x0]',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Dynamic Variable Assignment with 2 variables 2 times chained.', optimize=True)