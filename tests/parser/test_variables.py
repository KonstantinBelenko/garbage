from src.parser import ASTParser, NodeType
import unittest

class TestVariables(unittest.TestCase):

    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_variable_declaration(self):
        ast = self.ast_parser.parse('let x = 42;')
        self.assertDictEqual(ast, {
            "type": NodeType.PROGRAM,
            "body": [
                {
                    "type": NodeType.VARIABLE_STATEMENT,
                    "declarations": [
                        {
                            "type": NodeType.VARIABLE_DECLARATION,
                            "id": {
                                "type": NodeType.IDENTIFIER,
                                "name": "x"
                            },
                            "init": {
                                "type": NodeType.NUMERIC_LITERAL,
                                "value": 42
                            }
                        }
                    ]
                }
            ]
        })
    
    def test_multiple_variable_declarations(self):
        ast = self.ast_parser.parse('''
            let x = 42;
            let y = 42;
            let c = x + y;
        ''')
        self.assertDictEqual(ast, {
            "type": NodeType.PROGRAM,
            "body": [
                {
                    "type": NodeType.VARIABLE_STATEMENT,
                    "declarations": [
                        {
                            "type": NodeType.VARIABLE_DECLARATION,
                            "id": {
                                "type": NodeType.IDENTIFIER,
                                "name": "x"
                            },
                            "init": {
                                "type": NodeType.NUMERIC_LITERAL,
                                "value": 42
                            }
                        }
                    ]
                },
                {
                    "type": NodeType.VARIABLE_STATEMENT,
                    "declarations": [
                        {
                            "type": NodeType.VARIABLE_DECLARATION,
                            "id": {
                                "type": NodeType.IDENTIFIER,
                                "name": "y"
                            },
                            "init": {
                                "type": NodeType.NUMERIC_LITERAL,
                                "value": 42
                            }
                        }
                    ]
                },
                {
                    "type": NodeType.VARIABLE_STATEMENT,
                    "declarations": [
                        {
                            "type": NodeType.VARIABLE_DECLARATION,
                            "id": {
                                "type": NodeType.IDENTIFIER,
                                "name": "c"
                            },
                            "init": {
                                "type": NodeType.BINARY_EXPRESSION,
                                "operator": "+",
                                "left": {
                                    "type": NodeType.IDENTIFIER,
                                    "name": "x"
                                },
                                "right": {
                                    "type": NodeType.IDENTIFIER,
                                    "name": "y"
                                }
                            }
                        }
                    ]
                }
            ]
        })
        
    def test_variable_declaration_multiple_declarations(self):
        ast = self.ast_parser.parse('let x, y;')
        self.assertDictEqual(ast, {
            "type": NodeType.PROGRAM,
            "body": [
                {
                    "type": NodeType.VARIABLE_STATEMENT,
                    "declarations": [
                        {
                            "type": NodeType.VARIABLE_DECLARATION,
                            "id": {
                                "type": NodeType.IDENTIFIER,
                                "name": "x"
                            },
                            "init": None
                        },
                        {
                            "type": NodeType.VARIABLE_DECLARATION,
                            "id": {
                                "type": NodeType.IDENTIFIER,
                                "name": "y"
                            },
                            "init": None
                        }
                    ]
                }
            ]
        })
    
    def test_variable_declaration_multiple_declarations_and_assignment(self):
        ast = self.ast_parser.parse('let x, y = 42;')
        self.assertDictEqual(ast, {
            "type": NodeType.PROGRAM,
            "body": [
                {
                    "type": NodeType.VARIABLE_STATEMENT,
                    "declarations": [
                        {
                            "type": NodeType.VARIABLE_DECLARATION,
                            "id": {
                                "type": NodeType.IDENTIFIER,
                                "name": "x"
                            },
                            "init": None
                        },
                        {
                            "type": NodeType.VARIABLE_DECLARATION,
                            "id": {
                                "type": NodeType.IDENTIFIER,
                                "name": "y"
                            },
                            "init": {
                                "type": NodeType.NUMERIC_LITERAL,
                                "value": 42
                            }
                        }
                    ]
                }
            ]
        })

if __name__ == '__main__':
    unittest.main()