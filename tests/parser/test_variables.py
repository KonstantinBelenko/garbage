from src.parser import ASTParser, NT, Node
import unittest

class TestVariables(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_variable_declaration(self):
        ast = self.ast_parser.parse('let x = 42;')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.VARIABLE_STATEMENT, children=[
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='x'),
                        Node(NT.NUMERIC_LITERAL, value=42)
                    ])
                ])
            ])
        )
    
    def test_variable_declaration_and_assignment(self):
        ast = self.ast_parser.parse('let x = 42; let y = x * 2;')
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.VARIABLE_STATEMENT, children=[
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='x'),
                        Node(NT.NUMERIC_LITERAL, value=42)
                    ])
                ]),
                Node(NT.VARIABLE_STATEMENT, children=[
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='y'),
                        Node(NT.BINARY_EXPRESSION, value='*', children=[
                            Node(NT.IDENTIFIER, value='x'),
                            Node(NT.NUMERIC_LITERAL, value=2)
                        ])
                    ])
                ])
            ])
        )
        
    def test_multiple_variable_declarations(self):
        ast = self.ast_parser.parse('''
            let x = 42;
            let y = 42;
            let c = x + y;
        ''')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.VARIABLE_STATEMENT, children=[
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='x'),
                        Node(NT.NUMERIC_LITERAL, value=42)
                    ])
                ]),
                Node(NT.VARIABLE_STATEMENT, children=[
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='y'),
                        Node(NT.NUMERIC_LITERAL, value=42)
                    ])
                ]),
                Node(NT.VARIABLE_STATEMENT, children=[
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='c'),
                        Node(NT.BINARY_EXPRESSION, value='+', children=[
                            Node(NT.IDENTIFIER, value='x'),
                            Node(NT.IDENTIFIER, value='y')
                        ])
                    ])
                ])
            ])
        )
        
    def test_variable_declaration_multiple_declarations(self):
        ast = self.ast_parser.parse('let x, y = 42;')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.VARIABLE_STATEMENT, children=[
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='x')
                    ]),
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='y'),
                        Node(NT.NUMERIC_LITERAL, value=42)
                    ])
                ])
            ]),
        )
    
if __name__ == '__main__':
    unittest.main()