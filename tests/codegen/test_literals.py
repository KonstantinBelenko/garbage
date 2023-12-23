from src.codegen import CodeGenerator, CodeGen_v2
from src.parser import ASTParser, NT, Node
import unittest

class TestCodegenLiterals(unittest.TestCase):

    def setUp(self):
        self.codegen = CodeGen_v2()
        self.parser = ASTParser()
        self.maxDiff = None

    def _gen(self, code: str) -> tuple[Node, str]:
        ast = self.parser.parse(code)
        code = self.codegen.generate(ast)
        return ast, code
    
    def _gen_data_node_asm(self, code: str) -> tuple[Node, str]:
        ast = self.parser.parse(code)
        code = self.codegen.generate_data(ast)
        return ast, code
    
    def _gen_text_node_asm(self, code: str) -> tuple[Node, str]:
        ast = self.parser.parse(code)
        code = self.codegen.generate_text(ast)
        return ast, code
    
    def test_literal_number(self):
        ast, code = self._gen_data_node_asm('42;')
        self.assertEqual(
            code,
            [
                '.data',
                '.align 3',
                'literal_0: .word 42'
            ],
            ast
        )

    def test_two_literal_numbers(self):
        ast, code = self._gen_data_node_asm('42;5;')
        self.assertEqual(
            code,
            [
                '.data',
                '.align 3',
                'literal_0: .word 42',
                '.align 3',
                'literal_1: .word 5'
            ],
            ast
        )
    
    def test_one_string_literal(self):
        ast, code = self._gen_data_node_asm('"hello world";')
        self.assertEqual(
            code,
            [
                '.data',
                '.align 3',
                'literal_0: .asciz "hello world"'
            ],
            ast
        )
    
    def test_two_string_literals(self):
        ast, code = self._gen_data_node_asm('"hello world";"hello world";')
        self.assertEqual(
            code,
            [
                '.data',
                '.align 3',
                'literal_0: .asciz "hello world"',
                '.align 3',
                'literal_1: .asciz "hello world"'
            ],
            ast
        )
        
    def test_number_and_string_literals(self):
        ast, code = self._gen_data_node_asm('"hello world";42;')
        self.assertEqual(
            code,
            [
                '.data',
                '.align 3',
                'literal_0: .asciz "hello world"',
                '.align 3',
                'literal_1: .word 42'
            ],
            ast
        )
    
if __name__ == '__main__':
    unittest.main()