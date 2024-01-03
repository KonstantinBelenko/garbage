from src.parser import ASTParser, NT, Node
import unittest

if 'unittest.util' in __import__('sys').modules:
    # Show full diff in self.assertEqual.
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

class TestLoops(unittest.TestCase):
    
    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_while(self):
        ast = self.ast_parser.parse("""
            while (x > 10) {
                x -= 1;
            }
        """)
        self.assertEqual(ast, Node(NT.PROGRAM, children=[
            Node(NT.WHILE_LOOP_STATEMENT, children=[
                Node(NT.BINARY_EXPRESSION, value='>', children=[
                    Node(NT.IDENTIFIER, value='x'),
                    Node(NT.NUMERIC_LITERAL, value=10)
                ]),
                Node(NT.BLOCK_STATEMENT, children=[
                    Node(NT.EXPRESSION_STATEMENT, children=[
                        Node(NT.ASSIGNMENT_EXPRESSION, value='-=', children=[
                            Node(NT.IDENTIFIER, value='x'),
                            Node(NT.NUMERIC_LITERAL, value=1)
                        ])
                    ])
                ])
            ]),
        ]))

    def test_do_while(self):
        ast = self.ast_parser.parse("""
            do {
                x -= 1;
            } while (x > 10);
        """)
        self.assertEqual(ast, Node(NT.PROGRAM, children=[
            Node(NT.DO_WHILE_LOOP_STATEMENT, children=[
                Node(NT.BLOCK_STATEMENT, children=[
                    Node(NT.EXPRESSION_STATEMENT, children=[
                        Node(NT.ASSIGNMENT_EXPRESSION, value='-=', children=[
                            Node(NT.IDENTIFIER, value='x'),
                            Node(NT.NUMERIC_LITERAL, value=1)
                        ])
                    ])
                ]),
                Node(NT.BINARY_EXPRESSION, value='>', children=[
                    Node(NT.IDENTIFIER, value='x'),
                    Node(NT.NUMERIC_LITERAL, value=10)
                ])
            ]),
        ]))
    
    
    def test_for(self):
        ast = self.ast_parser.parse("""
            for (let i = 0; i < 10; i += 1) {
                _print(i);
            }
        """)
        self.assertEqual(ast, Node(NT.PROGRAM, children=[
            Node(NT.FOR_LOOP_STATEMENT, children=[
                Node(NT.VARIABLE_STATEMENT, children=[
                    Node(NT.VARIABLE_DECLARATION, children=[
                        Node(NT.IDENTIFIER, value='i'),
                        Node(NT.NUMERIC_LITERAL, value=0)
                    ])
                ]),
                Node(NT.BINARY_EXPRESSION, value='<', children=[
                    Node(NT.IDENTIFIER, value='i'),
                    Node(NT.NUMERIC_LITERAL, value=10)
                ]),
                Node(NT.ASSIGNMENT_EXPRESSION, value='+=', children=[
                    Node(NT.IDENTIFIER, value='i'),
                    Node(NT.NUMERIC_LITERAL, value=1)
                ]),
                Node(NT.BLOCK_STATEMENT, children=[
                    Node(NT.CMD_PRINT_STATEMENT, children=[
                        Node(NT.IDENTIFIER, value='i')
                    ])
                ]),
            ]),
        ]))

    def test_empty_for(self):
        ast = self.ast_parser.parse("""
            for (;;) {
                _print(i);
            }
        """)
        self.assertEqual(ast, Node(NT.PROGRAM, children=[
            Node(NT.FOR_LOOP_STATEMENT, children=[
                None, 
                None, 
                None,
                Node(NT.BLOCK_STATEMENT, children=[
                    Node(NT.CMD_PRINT_STATEMENT, children=[
                        Node(NT.IDENTIFIER, value='i')
                    ])
                ]),
            ]),
        ]))

if __name__ == '__main__':
    unittest.main()