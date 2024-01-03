from src.parser import ASTParser, NT, Node
import unittest

class TestIfStatements(unittest.TestCase):
    
    def setUp(self):
        self.ast_parser = ASTParser()
    
    def test_if(self):
        ast = self.ast_parser.parse("""
            if (x) {
                x = 1;
            }
        """)
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.IF_STATEMENT, children=[
                    Node(NT.IDENTIFIER, value='x'),
                    Node(NT.BLOCK_STATEMENT, children=[
                        Node(NT.EXPRESSION_STATEMENT, children=[
                            Node(NT.ASSIGNMENT_EXPRESSION, '=', children=[
                                Node(NT.IDENTIFIER, 'x'),
                                Node(NT.NUMERIC_LITERAL, 1)
                            ])
                        ])
                    ]),
                ])
            ])
        )
    
    def test_ifelse(self):
        ast = self.ast_parser.parse("""
            if (x) {
                x = 1;
            } else {
                x = 2;
            }
        """)
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.IF_STATEMENT, children=[
                    Node(NT.IDENTIFIER, value='x'),
                    Node(NT.BLOCK_STATEMENT, children=[
                        Node(NT.EXPRESSION_STATEMENT, children=[
                            Node(NT.ASSIGNMENT_EXPRESSION, '=', children=[
                                Node(NT.IDENTIFIER, 'x'),
                                Node(NT.NUMERIC_LITERAL, 1)
                            ])
                        ])
                    ]),
                    Node(NT.BLOCK_STATEMENT, children=[
                        Node(NT.EXPRESSION_STATEMENT, children=[
                            Node(NT.ASSIGNMENT_EXPRESSION, '=', children=[
                                Node(NT.IDENTIFIER, 'x'),
                                Node(NT.NUMERIC_LITERAL, 2)
                            ])
                        ])
                    ])
                ])
            ])
        )
    
    def test_if_noblock(self):
        ast = self.ast_parser.parse("""
            if (x) x = 1;
        """)
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.IF_STATEMENT, children=[
                    Node(NT.IDENTIFIER, value='x'),
                    Node(NT.EXPRESSION_STATEMENT, children=[
                        Node(NT.ASSIGNMENT_EXPRESSION, '=', children=[
                            Node(NT.IDENTIFIER, 'x'),
                            Node(NT.NUMERIC_LITERAL, 1)
                        ])
                    ])
                ])
            ])
        )
    
    def test_if_noblock_nested(self):
        ast = self.ast_parser.parse("""
            if (x) if (y) {} else {}
        """)
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.IF_STATEMENT, children=[
                    Node(NT.IDENTIFIER, 'x'),
                    Node(NT.IF_STATEMENT, children=[
                        Node(NT.IDENTIFIER, 'y'),
                        Node(NT.BLOCK_STATEMENT),
                        Node(NT.BLOCK_STATEMENT),
                    ])
                ])
            ])
        )

    def test_if_noblock_nested2(self):
        ast = self.ast_parser.parse("""
            if (x) if (y) {} else {} else {}
        """)
        self.assertEqual(
            ast, 
            Node(NT.PROGRAM, children=[
                Node(NT.IF_STATEMENT, children=[
                    Node(NT.IDENTIFIER, 'x'),
                    Node(NT.IF_STATEMENT, children=[
                        Node(NT.IDENTIFIER, 'y'),
                        Node(NT.BLOCK_STATEMENT),
                        Node(NT.BLOCK_STATEMENT),
                    ]),
                    Node(NT.BLOCK_STATEMENT),
                ])
            ])
        )

if __name__ == '__main__':
    unittest.main()