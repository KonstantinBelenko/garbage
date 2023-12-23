import unittest
from src.parser import ASTParser, NT, Node


class TestAssignment(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_assignment(self):
        ast = self.ast_parser.parse('x = 42;')
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.ASSIGNMENT_EXPRESSION, '=', children=[
                        Node(NT.IDENTIFIER, value='x'),
                        Node(NT.NUMERIC_LITERAL, value=42)
                    ])
                ])
            ])
        )
    
    def test_chained_assignment(self):
        ast = self.ast_parser.parse('x = y = 42;')
        self.assertEqual(
            ast,
            Node(NT.PROGRAM, children=[
                Node(NT.EXPRESSION_STATEMENT, children=[
                    Node(NT.ASSIGNMENT_EXPRESSION, value='=', children=[
                        Node(NT.IDENTIFIER, 'x'),
                        Node(NT.ASSIGNMENT_EXPRESSION, value='=', children=[
                            Node(NT.IDENTIFIER, 'y'),
                            Node(NT.NUMERIC_LITERAL, 42)
                        ])
                    ])
                ])
            ])
        )

if __name__ == '__main__':
    unittest.main()