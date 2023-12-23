from src.parser import ASTParser, NT, Node
import unittest

class TestBlockStatements(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
    
    def test_block_statement(self):
        ast = self.ast_parser.parse('{ 42; }')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.BLOCK_STATEMENT, children=[
                    Node(NT.EXPRESSION_STATEMENT, children=[
                        Node(NT.NUMERIC_LITERAL, value=42)
                    ])
                ])
            ])
        )
        
    def test_empty_block_statement(self):
        ast = self.ast_parser.parse('{}')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.BLOCK_STATEMENT, children=[])
            ])
        )
        
    def test_nested_block_statement(self):
        ast = self.ast_parser.parse('{ 42; { "hello"; } }')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.BLOCK_STATEMENT, children=[
                    Node(NT.EXPRESSION_STATEMENT, children=[
                        Node(NT.NUMERIC_LITERAL, value=42)
                    ]),
                    Node(NT.BLOCK_STATEMENT, children=[
                        Node(NT.EXPRESSION_STATEMENT, children=[
                            Node(NT.STRING_LITERAL, value='hello')
                        ])
                    ])
                ])
            ])
        )

if __name__ == '__main__':
    unittest.main()