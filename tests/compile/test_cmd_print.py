from src.compiler import compile_test
import subprocess
import unittest
import os

class TestCompileCmdPrint(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_print_string_literal(self):
        try:
            out_file = compile_test('_print("Hi!");')
            absolute_file_path = os.path.abspath(out_file)
            
            self.assertEqual(
                subprocess.check_output([absolute_file_path]).decode('utf-8'),
                'Hi!'
            )
        except Exception as e:
            self.fail(e)
            
    def test_print_numeric_literal(self):
        try:
            out_file = compile_test('_print(123);')
            absolute_file_path = os.path.abspath(out_file)
            
            output = subprocess.check_output([absolute_file_path]).decode('utf-8')
            print('OUTPUT:', output)
            
            self.assertEqual(
                output,
                '123\n'
            )
        except Exception as e:
            self.fail(e)

if __name__ == '__main__':
    unittest.main()