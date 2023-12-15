from src.shared_utils import verify_codegen

def test():
    print("Running codegen black statement test...")
    
    verify_codegen('''
    
    ''', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    literal_0: .word 46',
        '    literal_1: .word 23',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'Block statements')