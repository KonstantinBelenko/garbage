from src.parser import ASTParser, NT, Node
import unittest

class TestCommandPrintStatement(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_print_string(self):
        ast = self.ast_parser.parse('_print("Hello, world!");')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.CMD_PRINT_STATEMENT, children=[
                    Node(NT.STRING_LITERAL, value='Hello, world!')
                ])
            ])
        )
    
    def test_print_numeric_literal(self):
        ast = self.ast_parser.parse('_print(42);')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.CMD_PRINT_STATEMENT, children=[
                    Node(NT.NUMERIC_LITERAL, value=42)
                ])
            ])
        )
    
    def test_print_expression(self):
        ast = self.ast_parser.parse('_print(5 + 15);')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.CMD_PRINT_STATEMENT, children=[
                    Node(NT.NUMERIC_LITERAL, value=20)
                ])
            ])
        )
    
    def test_print_variable_expression(self):
        ast = self.ast_parser.parse('''
            let x = 55;
            _print(x + 42);
            ''')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.VARIABLE_STATEMENT, children=[
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='x'),
                        Node(NT.NUMERIC_LITERAL, value=55)
                    ])
                ]),
                Node(NT.CMD_PRINT_STATEMENT, children=[
                    Node(NT.BINARY_EXPRESSION, value='+', children=[
                        Node(NT.IDENTIFIER, value='x'),
                        Node(NT.NUMERIC_LITERAL, value=42)
                    ])
                ])
            ])
        )
    
if __name__ == '__main__':
    unittest.main()