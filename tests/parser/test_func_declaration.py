from src.parser import ASTParser, NT, Node
import unittest

if 'unittest.util' in __import__('sys').modules:
    # Show full diff in self.assertEqual.
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

class TestFunctionDeclaration(unittest.TestCase):
    
    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_while(self):
        ast = self.ast_parser.parse("""
            def square(x) {
                return x * x;
            }
        """)
        self.assertEqual(ast, Node(NT.PROGRAM, children=[
            Node(NT.FUNCTION_DECLARATION_STATEMENT, children=[
                Node(NT.IDENTIFIER, 'square'),
                Node(NT.FUNCTION_PARAMETERS, children=[
                    Node(NT.IDENTIFIER, 'x')
                ]),
                Node(NT.BLOCK_STATEMENT, children=[
                    Node(NT.RETURN_STATEMENT, children=[
                        Node(NT.BINARY_EXPRESSION, '*', children=[
                            Node(NT.IDENTIFIER, 'x'),
                            Node(NT.IDENTIFIER, 'x')
                        ])
                    ])
                ]),
            ])
        ]))

    def test_empty(self):
        ast = self.ast_parser.parse("""
            def empty() {
                return;
            }
        """)
        self.assertEqual(ast, Node(NT.PROGRAM, children=[
            Node(NT.FUNCTION_DECLARATION_STATEMENT, children=[
                Node(NT.IDENTIFIER, 'empty'),
                Node(NT.FUNCTION_PARAMETERS),
                Node(NT.BLOCK_STATEMENT, children=[
                    Node(NT.RETURN_STATEMENT)
                ]),
            ])
        ]))
    
    def test_multiple_parameters(self):
        ast = self.ast_parser.parse("""
            def add(x, y) {
                return x + y;
            }
        """)
        self.assertEqual(ast, Node(NT.PROGRAM, children=[
            Node(NT.FUNCTION_DECLARATION_STATEMENT, children=[
                Node(NT.IDENTIFIER, 'add'),
                Node(NT.FUNCTION_PARAMETERS, children=[
                    Node(NT.IDENTIFIER, 'x'),
                    Node(NT.IDENTIFIER, 'y')
                ]),
                Node(NT.BLOCK_STATEMENT, children=[
                    Node(NT.RETURN_STATEMENT, children=[
                        Node(NT.BINARY_EXPRESSION, '+', children=[
                            Node(NT.IDENTIFIER, 'x'),
                            Node(NT.IDENTIFIER, 'y')
                        ])
                    ])
                ]),
            ])
        ]))

if __name__ == '__main__':
    unittest.main()