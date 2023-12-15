import json

from ast_parser import Parser

from tests.ast.test_literals import test as literals_test
from tests.ast.test_statement_list import test as statement_list_test
from tests.ast.test_block_statements import test as block_statements_test
from tests.ast.test_empty_statements import test as empty_statements_test
from tests.ast.test_math import test as math_test
from tests.ast.test_assignment import test as assignment_test
from tests.ast.test_variables import test as variables_test
from tests.ast.test_math_optimized import test as math_optimized_test
from tests.ast.test_cmd_print_statements import test as cmd_print_statements_test

ast_tests = [
    # -----------------
    # Syntax tests
    literals_test, statement_list_test, block_statements_test, 
    empty_statements_test, assignment_test, variables_test,
    cmd_print_statements_test,
    
    # -----------------
    # Semantic tests
    math_test, math_optimized_test
]

from tests.codegen.test_codegen_literals import test as codegen_test_literals
from tests.codegen.test_codegen_statement_list import test as codegen_test_statement_list
from tests.codegen.test_codegen_math import test as codegen_test_math
from tests.codegen.test_codegen_variables import test as codegen_test_variables
from tests.codegen.test_codegen_cmdprint import test as codegen_test_cmdprint

codegen_tests = [
    codegen_test_literals, codegen_test_statement_list, codegen_test_math, codegen_test_variables,
    codegen_test_cmdprint
]

def manual_test():
    example = '''
    42;
    '''
    
    parser = Parser()
    output = parser.parse(example)
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    for test in ast_tests:
        test()
        
    print('\n---')
    
    for test in codegen_tests:
        test()
    
    # manual_test()