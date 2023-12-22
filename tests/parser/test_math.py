import unittest
from src.parser import ASTParser, NodeType
from src.shared_utils import verify


class TestMath(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_addition(self):
        ast = self.ast_parser.parse('2 + 2;')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.NUMERIC_LITERAL,
                        'value': 4
                    }
                }
            ]
        })
    
    def test_subtraction(self):
        ast = self.ast_parser.parse('3 - 2;')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.NUMERIC_LITERAL,
                        'value': 1
                    }
                }
            ]
        })
    
    def test_multiplication(self):
        ast = self.ast_parser.parse('2 * 2;')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.NUMERIC_LITERAL,
                        'value': 4
                    }
                }
            ]
        })
    
    def test_division(self):
        ast = self.ast_parser.parse('4 / 2;')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.NUMERIC_LITERAL,
                        'value': 2
                    }
                }
            ]
        })
    
    def test_parenteses(self):
        ast = self.ast_parser.parse('(2 + 2) * 2;')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.NUMERIC_LITERAL,
                        'value': 8
                    }
                }
            ]
        })


if __name__ == '__main__':
    unittest.main()