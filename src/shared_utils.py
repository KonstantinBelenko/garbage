from deepdiff import DeepDiff
from src.ast_parser import Parser
from src.codegen import CodeGenerator
import subprocess
import tempfile

import json

def verify(input: str, expected: dict, name: str = None, optimize: bool = False) -> None:
    parser = Parser()
    result = None
    
    if optimize:
        result = parser.parse_optimized(input)    
    else:
        result = parser.parse(input)
    
    # Convert to dict
    
    diff = DeepDiff(expected, result)
    diff_json = diff.to_json()
    diff_pretty = json.dumps(json.loads(diff_json), indent=4)
    
    if  diff != {}:
        print('\033[91m' + '✗' + '\033[0m', name or 'failed')
        print("Expected:\n", json.dumps(expected, indent=4))

        print("Actual:\n", json.dumps(result, indent=4))
        
        assert diff == {}, diff_pretty
    else:
        print('\033[92m' + '✓' + '\033[0m', name or 'passed')

def verify_codegen(inp: str, output_asm: list[str], name_str=None, optimize=False) -> None:
    parser = Parser()
    codegen = CodeGenerator()
    ast = None
    
    if optimize:
        ast = parser.parse_optimized(inp)
    else:
        ast = parser.parse(inp)
        
    asm = codegen.generate(ast)
    
    expected_output = '\n'.join(output_asm)
    
    if asm != expected_output:
        print('\033[91m' + '✗' + '\033[0m', name_str or 'failed')
        print("Expected:\n", expected_output)
        print("Actual:\n", asm)
        
        assert asm == expected_output
    else:
        temp_asm_file_path = 'temp.s'
        with open(temp_asm_file_path, 'w') as f:
            f.write(expected_output)
        
        # Assemble
        compile_result = subprocess.run(['as', '-g', temp_asm_file_path, '-o', 'temp.o'], capture_output=True)
        if compile_result.returncode != 0:
            print('\033[91m' + '✗' + '\033[0m', name_str or 'failed')
            print("Error compiling:\n", compile_result.stderr.decode('utf-8'))
            assert compile_result.returncode == 0
        
        # Get SDK path
        sdk_path_result = subprocess.run(['xcrun', '--sdk', 'macosx', '--show-sdk-path'], capture_output=True, text=True)
        if sdk_path_result.returncode != 0:
            print("Error getting SDK path:\n", sdk_path_result.stderr)
            assert sdk_path_result.returncode == 0
        sdk_path = sdk_path_result.stdout.strip()

        # Link
        link_command = ['ld', 'temp.o', '-o', 'temp', '-L' + sdk_path + '/usr/lib', '-lSystem', '-e', '_main', '-arch', 'arm64']
        link_result = subprocess.run(link_command, capture_output=True, text=True)
        if link_result.returncode != 0:
            print('\033[91m' + '✗' + '\033[0m', name_str or 'failed')
            print("Error linking:\n", link_result.stderr)
            assert link_result.returncode == 0
        
        print('\033[92m' + '✓' + '\033[0m', name_str or 'passed')
        

def assemble(file_in: str, file_out: str):
    compile_result = subprocess.run(['as', '-g', file_in, '-o', file_out], capture_output=True)
    if compile_result.returncode != 0:
        print("Error compiling:\n", compile_result.stderr.decode('utf-8'))
        assert compile_result.returncode == 0

def link(file_in: str, file_out: str):
    
    sdk_path_result = subprocess.run(['xcrun', '--sdk', 'macosx', '--show-sdk-path'], capture_output=True, text=True)
    if sdk_path_result.returncode != 0:
        print("Error getting SDK path:\n", sdk_path_result.stderr)
        assert sdk_path_result.returncode == 0
    sdk_path = sdk_path_result.stdout.strip()

    link_command = ['ld', file_in, '-o', file_out, '-L' + sdk_path + '/usr/lib', '-lSystem', '-e', '_main', '-arch', 'arm64']
    link_result = subprocess.run(link_command, capture_output=True, text=True)
    if link_result.returncode != 0:
        print("Error linking:\n", link_result.stderr)
        assert link_result.returncode == 0