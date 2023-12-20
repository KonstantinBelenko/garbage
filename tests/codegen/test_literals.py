from src.codegen import CodeGenerator
from src.parser import NodeType
import unittest

class TestCodegenLiterals(unittest.TestCase):

    def setUp(self):
        self.codegen = CodeGenerator()
        self.maxDiff = None

    
    def test_literal_int(self):
        asm = self.codegen.generate({
            "type": "Program",
            "body": [
                {
                    "type": NodeType.EXPRESSION_STATEMENT,
                    "body": {
                        "type": NodeType.NUMERIC_LITERAL,
                        "value": 42
                    }
                }
            ]
        })
        print("AAAA:", asm)
        self.assertEqual(
            asm,
            [
                '.global _main',
                '.align 3',
                '.data',
                'literal_0: .word 42',
                '.text',
                '_main:',
                'mov x0, #0',
                'mov x16, #1',
                'svc 0',
            ]   
        )     

    def test_literal_string(self):
        asm = self.codegen.generate({
            "type": "Program",
            "body": [
                {
                    "type": NodeType.EXPRESSION_STATEMENT,
                    "body": {
                        "type": NodeType.STRING_LITERAL,
                        "value": "hello world"
                    }
                }
            ]
        })
        self.assertEqual(
            asm,
            [
                '.global _main',
                '.align 3',
                '.data',
                'literal_0: .asciz "hello world"',
                '.text',
                '_main:',
                'mov x0, #0',
                'mov x16, #1',
                'svc 0',
            ]   
        )

if __name__ == '__main__':
    unittest.main()