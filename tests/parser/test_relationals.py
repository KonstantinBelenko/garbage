from src.parser import ASTParser, NT, Node
import unittest

class TestRelationals(unittest.TestCase):
    
    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_more(self):
        ast = self.ast_parser.parse("""
            x > 0;
        """)
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.BINARY_EXPRESSION, '>', [
                        Node(NT.IDENTIFIER, 'x'),
                        Node(NT.NUMERIC_LITERAL, 0)
                    ])
                ])
            ]),
            ast
        )
    
    def test_less_or_equal(self):
        ast = self.ast_parser.parse("""
            x < 5 + 10;
        """)
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.BINARY_EXPRESSION, '<', [
                        Node(NT.IDENTIFIER, 'x'),
                        Node(NT.NUMERIC_LITERAL, 15)
                    ])
                ])
            ]),
            ast
        )

if __name__ == '__main__':
    unittest.main()