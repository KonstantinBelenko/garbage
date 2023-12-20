import unittest
from src.parser import ASTParser, NodeType

class TestEmptyStatements(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
    
    def test_empty_statement(self):
        ast = self.ast_parser.parse(';')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.EMPTY_STATEMENT,
                }
            ]
        })
    
    def test_multiple_empty_statements(self):
        ast = self.ast_parser.parse(';;')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.EMPTY_STATEMENT,
                },
                {
                    'type': NodeType.EMPTY_STATEMENT,
                }
            ]
        })

if __name__ == '__main__':
    unittest.main()