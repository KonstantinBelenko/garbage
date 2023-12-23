from src.parser import ASTParser, NT, Node
import unittest

class TestLiterals(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
    
    def test_literal_int(self):
        ast = self.ast_parser.parse("42;")
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.NUMERIC_LITERAL, value=42)
                ])
            ])
        )

    def test_literal_string(self):
        ast = self.ast_parser.parse('"hello world";')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.STRING_LITERAL, value="hello world")
                ])
            ])
        )

    def test_literal_string_single_quote(self):
        ast = self.ast_parser.parse("'hello world';")
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.STRING_LITERAL, value="hello world")
                ])
            ])
        )

if __name__ == '__main__':
    unittest.main()