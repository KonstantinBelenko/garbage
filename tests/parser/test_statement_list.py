from src.parser import ASTParser, NT, Node
import unittest


class TestStatementLists(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_statement_list(self):
        ast = self.ast_parser.parse('''
            "Hello World!";
            42;
            'Hello World!';
            _print("Hi!");
        ''')
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.STRING_LITERAL, value='Hello World!')
                ]),
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.NUMERIC_LITERAL, value=42)
                ]),
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.STRING_LITERAL, value='Hello World!')
                ]),
                Node(NT.CMD_PRINT_STATEMENT, children=[
                    Node(NT.STRING_LITERAL, value='Hi!')
                ])
            ])
        )
    
    def test_empty_statement_list(self):
        ast = self.ast_parser.parse(';')
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.EMPTY_STATEMENT)
            ])
        )
    
if __name__ == '__main__':
    unittest.main()