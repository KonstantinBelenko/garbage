from shared_utils import verify_codegen

def test():
    print("Running codegen literals test...")
    
    verify_codegen('_print("hello world");', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    literal_0: .asciz "hello world"',
        '',
        '.text',
        '_main:',
        '    adrp x6, literal_0@PAGE',
        '    add x6, x6, literal_0@PAGEOFF',
        '    mov x0, #1',
        '    mov x1, x6',
        '    mov x2, #11',
        '    mov x16, #4',
        '    svc 0',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Print literal string')
    
    # verify_codegen('_print(69);', [
    #     '.global _main',
    #     '.align 3',
    #     '',
    #     '.data',
    #     '    literal_0: .asciz "hello world"',
    #     '',
    #     '.text',
    #     '_main:',
    #     '    adrp x6, literal_0@PAGE',
    #     '    add x6, x6, literal_0@PAGEOFF',
    #     '    mov x0, #1',
    #     '    mov x1, x6',
    #     '    mov x2, #11',
    #     '    mov x16, #4',
    #     '    svc 0',
    #     '    mov x0, #0',
    #     '    mov x16, #1',
    #     '    svc 0',
    # ], 'Print literal number')