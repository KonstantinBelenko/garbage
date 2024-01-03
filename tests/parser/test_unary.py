from src.parser import ASTParser, NT, Node
import unittest

class TestUnary(unittest.TestCase):
    
    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_unary_minus(self):
        ast = self.ast_parser.parse("""
            -x;
        """)
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.UNARY_EXPRESSION, '-', [
                        Node(NT.IDENTIFIER, 'x')
                    ])
                ])
            ]),
            ast
        )
    
    def test_unary_not(self):
        ast = self.ast_parser.parse("""
            !x;
        """)
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.UNARY_EXPRESSION, '!', [
                        Node(NT.IDENTIFIER, 'x')
                    ])
                ])
            ]),
            ast
        )

    def test_double_unary_minus(self):
        ast = self.ast_parser.parse("""
            --x;
        """)
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.UNARY_EXPRESSION, '-', [
                        Node(NT.UNARY_EXPRESSION, '-', [
                            Node(NT.IDENTIFIER, 'x')
                        ])
                    ])
                ])
            ]),
            ast
        )


if __name__ == '__main__':
    unittest.main()