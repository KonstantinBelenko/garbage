# from src.codegen import CodeGenerator
# from src.parser import NT
# import unittest

# class TestCodegenStatementList(unittest.TestCase):

#     def setUp(self):
#         self.codegen = CodeGenerator()
#         self.maxDiff = None

    
#     def test_statement_list(self):
#         asm = self.codegen.generate({
#             'type': NT.PROGRAM,
#             'body': [
#                 {
#                     'type': NT.EXPRESSION_STATEMENT,
#                     'body': {
#                         'type': NT.STRING_LITERAL,
#                         'value': 'Hello World!'
#                     }
#                 },
#                 {
#                     'type': NT.EXPRESSION_STATEMENT,
#                     'body': {
#                         'type': NT.NUMERIC_LITERAL,
#                         'value': 42
#                     }
#                 },
#                 {
#                     'type': NT.CMD_PRINT_STATEMENT,
#                     'body': {
#                         'type': NT.STRING_LITERAL,
#                         'value': 'Hi!'
#                     }
#                 }
#             ]
#         })
#         self.assertEqual(
#             asm,
#             [
#                 '.global _main',
#                 'print_string:',
#                 'ldrb w2, [x1]',
#                 'cmp w2, #0',
#                 'beq _print_string_end',
#                 'mov x3, x1',
#                 'mov x0, 1',
#                 'mov x2, 1',
#                 'mov x16, 4',
#                 'svc 0',
#                 'mov x1, x3',
#                 'add x1, x1, #1',
#                 'b print_string',
#                 '_print_string_end:',
#                 'ret',
#                 '.data',
#                 '.align 3',
#                 'literal_0: .asciz "Hello World!"',
#                 '.align 3',
#                 'literal_1: .word 42',
#                 '.align 3',
#                 'literal_2: .asciz "Hi!"',
#                 '.text',
#                 '_main:',
#                 'adrp x1, literal_2@PAGE',
#                 'add x1, x1, literal_2@PAGEOFF',
#                 'bl print_string',
#                 'mov x0, #0',
#                 'mov x16, #1',
#                 'svc 0',
#             ]   
#         )     

# if __name__ == '__main__':
#     unittest.main()