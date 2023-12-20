import unittest
from src.parser import ASTParser, NodeType


class TestAssignment(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_assignment(self):
        ast = self.ast_parser.parse('x = 42;')
        self.assertDictEqual(ast, {
            "type": NodeType.PROGRAM,
            "body": [
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.ASSIGNMENT_EXPRESSION,
                        'operator': '=',
                        'left': {
                            'type': NodeType.IDENTIFIER,
                            'name': 'x'
                        },
                        'right': {
                            'type': NodeType.NUMERIC_LITERAL,
                            'value': 42
                        }
                    }
                }
            ]
        })
    
    def test_chained_assignment(self):
        ast = self.ast_parser.parse('x = y = 42;')
        self.assertDictEqual(ast, {
            "type": NodeType.PROGRAM,
            "body": [
                {
                    "type": NodeType.EXPRESSION_STATEMENT,
                    "body": {
                        "type": NodeType.ASSIGNMENT_EXPRESSION,
                        "operator": "=",
                        "left": {
                            "type": NodeType.IDENTIFIER,
                            "name": "x"
                        },
                        "right": {
                            "type": NodeType.ASSIGNMENT_EXPRESSION,
                            "operator": "=",
                            "left": {
                                "type": NodeType.IDENTIFIER,
                                "name": "y"
                            },
                            "right": {
                                "type": NodeType.NUMERIC_LITERAL,
                                "value": 42
                            }
                        }
                    }
                }
            ]
        })

if __name__ == '__main__':
    unittest.main()