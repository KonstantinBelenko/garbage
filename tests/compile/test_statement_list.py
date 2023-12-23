# from src.compiler import compile_test
# import unittest

# class TestCompileStatementList(unittest.TestCase):

#     def setUp(self):
#         self.maxDiff = None

#     def test_statement_list(self):
#         try:
#             compile_test('''
#                 "Hello World!";
#                 42;
#                 _print('Hi!');
#             ''')
#         except Exception as e:
#             self.fail(e)

# if __name__ == '__main__':
#     unittest.main()