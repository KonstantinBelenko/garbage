from src.parser import ASTParser, NodeType
import unittest

class TestBlockStatements(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
    
    def test_block_statement(self):
        ast = self.ast_parser.parse('{ 42; }')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.BLOCK_STATEMENT,
                    'body': [
                        {
                            'type': NodeType.EXPRESSION_STATEMENT,
                            'body': {
                                'type': NodeType.NUMERIC_LITERAL,
                                'value': 42
                            }
                        }
                    ]
                }
            ]
        })
        
    def test_empty_block_statement(self):
        ast = self.ast_parser.parse('{}')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.BLOCK_STATEMENT,
                    'body': []
                }
            ]
        })
        
    def test_nested_block_statement(self):
        ast = self.ast_parser.parse('{ 42; { "hello"; } }')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.BLOCK_STATEMENT,
                    'body': [
                        {
                            'type': NodeType.EXPRESSION_STATEMENT,
                            'body': {
                                'type': NodeType.NUMERIC_LITERAL,
                                'value': 42
                            }
                        },
                        {
                            'type': NodeType.BLOCK_STATEMENT,
                            'body': [
                                {
                                    'type': NodeType.EXPRESSION_STATEMENT,
                                    'body': {
                                        'type': NodeType.STRING_LITERAL,
                                        'value': 'hello'
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        })


if __name__ == '__main__':
    unittest.main()