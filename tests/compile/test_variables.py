from src.codegen import Codegen_V3
from src.parser import ASTParser
from src.compiler import compile_run
import unittest

if 'unittest.util' in __import__('sys').modules:
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

class TestCodegenVariables(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_variable(self):
        out, path = compile_run(Codegen_V3, 'let x = 42; let y = x; let z = x + y;')
        self.assertEqual(out.stdout, '')
        self.assertEqual(out.stderr, '')
        self.assertEqual(out.returncode, 0)

if __name__ == '__main__':
    unittest.main()