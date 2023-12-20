from src.compiler import compile_test
import unittest

class TestCompileLiterals(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_literal_int(self):
        compile_test('42;')

    def test_literal_string(self):
        compile_test('"hello world";')
    
    def test_literal_string_single_quote(self):
        compile_test("'hello world';")

if __name__ == '__main__':
    unittest.main()