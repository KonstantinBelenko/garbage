from src.codegen import CodeGenerator
from src.parser import NodeType
import unittest

class TestCodegenStatementList(unittest.TestCase):

    def setUp(self):
        self.codegen = CodeGenerator()
        self.maxDiff = None

    
    def test_statement_list(self):
        asm = self.codegen.generate({
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.STRING_LITERAL,
                        'value': 'Hello World!'
                    }
                },
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.NUMERIC_LITERAL,
                        'value': 42
                    }
                },
                {
                    'type': NodeType.CMD_PRINT_STATEMENT,
                    'body': {
                        'type': NodeType.STRING_LITERAL,
                        'value': 'Hi!'
                    }
                }
            ]
        })
        self.assertEqual(
            asm,
            [
                '.global _main',
                '.align 3',
                'print_string:',
                'ldrb w2, [x1]',
                'cmp w2, #0',
                'beq _print_string_end',
                'sub sp, sp, #16',
                'str x1, [sp]',
                'mov x0, 1',
                'mov x2, 1',
                'mov x16, 4',
                'svc 0',
                'ldr x1, [sp]',
                'add sp, sp, #16',
                'add x1, x1, #1',
                'b print_string',
                '_print_string_end:',
                'ret',
                '.data',
                'literal_0: .asciz "Hello World!"',
                'literal_1: .word 42',
                'literal_2: .asciz "Hi!"',
                '.text',
                '_main:',
                'adrp x1, literal_2@PAGE',
                'add x1, x1, literal_2@PAGEOFF',
                'bl print_string',
                'mov x0, #0',
                'mov x16, #1',
                'svc 0',
            ]   
        )     

if __name__ == '__main__':
    unittest.main()