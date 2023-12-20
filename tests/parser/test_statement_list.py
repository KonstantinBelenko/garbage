from src.parser import ASTParser, NodeType
import unittest
from src.shared_utils import verify


class TestStatementLists(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_statement_list(self):
        ast = self.ast_parser.parse('''
            "Hello World!";
            42;
            'Hello World!';
            _print("Hi!");
        ''')
        self.assertDictEqual(ast, {
            'type': NodeType.PROGRAM,
            'body': [
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.STRING_LITERAL,
                        'value': 'Hello World!'
                    }
                },
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.NUMERIC_LITERAL,
                        'value': 42
                    }
                },
                {
                    'type': NodeType.EXPRESSION_STATEMENT,
                    'body': {
                        'type': NodeType.STRING_LITERAL,
                        'value': 'Hello World!'
                    }
                },
                {
                    'type': NodeType.CMD_PRINT_STATEMENT,
                    'body': {
                        'type': NodeType.STRING_LITERAL,
                        'value': 'Hi!'
                    }
                }
            ]
        })
    
if __name__ == '__main__':
    unittest.main()