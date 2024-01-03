from src.parser import ASTParser, NT, Node
import unittest

class TestLiterals(unittest.TestCase):
    
    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_and(self):
        ast = self.ast_parser.parse("""
            x > 0 && true;
        """)
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.BINARY_EXPRESSION, '&&', [
                        Node(NT.BINARY_EXPRESSION, '>', [
                            Node(NT.IDENTIFIER, 'x'),
                            Node(NT.NUMERIC_LITERAL, 0)
                        ]),
                        Node(NT.BOOLEAN_LITERAL, True)
                    ])
                ])
            ]),
            ast
        )
    
    def test_or(self):
        ast = self.ast_parser.parse("""
            x > 0 || false;
        """)
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.BINARY_EXPRESSION, '||', [
                        Node(NT.BINARY_EXPRESSION, '>', [
                            Node(NT.IDENTIFIER, 'x'),
                            Node(NT.NUMERIC_LITERAL, 0)
                        ]),
                        Node(NT.BOOLEAN_LITERAL, False)
                    ])
                ])
            ]),
            ast
        )
    
    
if __name__ == '__main__':
    unittest.main()