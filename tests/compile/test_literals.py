from src.compiler import compile_test
import unittest

class TestCompileLiterals(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_literal_int(self):
        try:
            compile_test('42;')
        except Exception as e:
            self.fail(e)

    def test_literal_string(self):
        try:
            compile_test('"hello world";')
        except Exception as e:
            self.fail(e)
    
    def test_literal_string_single_quote(self):
        try:
            compile_test("'hello world';")
        except Exception as e:
            self.fail(e)

if __name__ == '__main__':
    unittest.main()