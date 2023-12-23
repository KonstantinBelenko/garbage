import unittest
from src.parser import ASTParser, NT, Node

class TestEmptyStatements(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
    
    def test_empty_statement(self):
        ast = self.ast_parser.parse(';')
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.EMPTY_STATEMENT)
            ])
        )
    
    def test_multiple_empty_statements(self):
        ast = self.ast_parser.parse(';;')
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.EMPTY_STATEMENT),
                Node(NT.EMPTY_STATEMENT)
            ])
        )

if __name__ == '__main__':
    unittest.main()