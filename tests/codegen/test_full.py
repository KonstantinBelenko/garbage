from src.codegen import CodeGen_v2
from src.parser import ASTParser, NT, Node
import unittest

class TestCodegenFull(unittest.TestCase):

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
        ast, code = self._gen('42;')
        self.assertEqual(
            code,
            [
                '.global _main',
                'terminate_program:',
                'mov x0, #0',
                'mov x16, #1',
                'svc 0',
                '.data',
                '.align 3',
                'literal_0: .word 42',
                '.text',
                '_main:',
                'b terminate_program'
            ],
            ast
        )
    
if __name__ == '__main__':
    unittest.main()