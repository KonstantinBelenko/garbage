from shared_utils import verify_codegen

def test():
    print("Running codegen literals test...")
    
    verify_codegen('46;', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    literal_0: .word 46',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'NumericLiteral')