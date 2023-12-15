from src.shared_utils import verify_codegen

def test():
    print("Running codegen statement list test...")
    
    verify_codegen('46; 23; 46;', [
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
    ], 'Numeric Literal')
    
    verify_codegen('''
        // strings
        \"Hello World!\";
        'Hello World!';
    ''', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    literal_0: .asciz "Hello World!"',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'String Literals')
    
    verify_codegen('''
        // strings
        \"Hello World!\";
        'Hello World!';
        
        /**
         * POOPOO PEEPEE
         */
        
        // numbers
        69;
        32;
        55;
        55;
    ''', [
        '.global _main',
        '.align 3',
        '',
        '.data',
        '    literal_0: .asciz "Hello World!"',
        '    literal_1: .word 69',
        '    literal_2: .word 32',
        '    literal_3: .word 55',
        '',
        '.text',
        '_main:',
        '    mov x0, #0',
        '    mov x16, #1',
        '    svc 0',
    ], 'String Literals and Numeric Literal')