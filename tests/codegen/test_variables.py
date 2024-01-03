from src.codegen import Codegen_V3
from src.parser import NT, Node, ASTParser
import unittest

if 'unittest.util' in __import__('sys').modules:
    # Show full diff in self.assertEqual.
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

class TestCodegenVariables(unittest.TestCase):

    def setUp(self):
        self.parser = ASTParser()
        self.maxDiff = None
        
    def test_variable(self):
        # let x = 42;
        # let y = x;
        # let z = x + y;
        asm = Codegen_V3(Node(NT.PROGRAM, children=[
            Node(NT.VARIABLE_STATEMENT, children=[
                Node(NT.VARIABLE_DECLARATION, children=[
                    Node(NT.IDENTIFIER, 'x'),
                    Node(NT.NUMERIC_LITERAL, '42')
                ])
            ]),
            Node(NT.VARIABLE_STATEMENT, children=[
                Node(NT.VARIABLE_DECLARATION, children=[
                    Node(NT.IDENTIFIER, 'y'),
                    Node(NT.IDENTIFIER, 'x')
                ])
            ]),
            Node(NT.VARIABLE_STATEMENT, children=[
                Node(NT.VARIABLE_DECLARATION, children=[
                    Node(NT.IDENTIFIER, 'z'),
                    Node(NT.BINARY_EXPRESSION, '+', children=[
                        Node(NT.IDENTIFIER, 'x'),
                        Node(NT.IDENTIFIER, 'y')
                    ])
                ])
            ])
        ])).compile()
        
        self.assertEqual(asm, [
            '.global: main',
            'main:',
            'sub sp, sp, #16',
            'mov w0, #42',
            'str w0, [sp, 12]',
            'ldr w0, [sp, 12]',
            'str w0, [sp, 8]',
            'ldr w1, [sp, 12]',
            'ldr w0, [sp, 8]',
            'add w0, w1, w0',
            'str w0, [sp, 4]',
            'mov w0, #0',
            'add sp, sp, #16',
            'ret',
        ])

if __name__ == '__main__':
    unittest.main()