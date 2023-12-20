from src.parser import ASTParser, NodeType
import unittest

class TestLiterals(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
    
    def test_literal_int(self):
        ast = self.ast_parser.parse("42;")
        self.assertDictEqual(ast, {
            "type": NodeType.PROGRAM,
            "body": [
                {
                    "type": NodeType.EXPRESSION_STATEMENT,
                    "body": {
                        "type": NodeType.NUMERIC_LITERAL,
                        "value": 42
                    }
                }
            ]
        })

    def test_literal_string(self):
        ast = self.ast_parser.parse('"hello world";')
        self.assertDictEqual(ast, {
            "type": NodeType.PROGRAM,
            "body": [
                {
                    "type": NodeType.EXPRESSION_STATEMENT,
                    "body": {
                        "type": NodeType.STRING_LITERAL,
                        "value": "hello world"
                    }
                }
            ]
        })

    def test_literal_string_single_quote(self):
        ast = self.ast_parser.parse("'hello world';")
        self.assertDictEqual(ast, {
            "type": NodeType.PROGRAM,
            "body": [
                {
                    "type": NodeType.EXPRESSION_STATEMENT,
                    "body": {
                        "type": NodeType.STRING_LITERAL,
                        "value": "hello world"
                    }
                }
            ]
        })

if __name__ == '__main__':
    unittest.main()