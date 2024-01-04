from src.parser import ASTParser
from src.shared_utils import assemble, link
from src.codegen import Codegen

from typing import Optional
import subprocess
import tempfile
import os
    
def compile(codegen: Codegen, code: str, asm_path: Optional[str] = None, obj_path: Optional[str] = None, out_path: Optional[str] = None):

    parser = ASTParser()
    
    ast = parser.parse(code)
    assembly: list[str] = codegen(ast).compile()

    random_tmp_dir = tempfile.TemporaryDirectory()
    asm_path = asm_path if asm_path else random_tmp_dir.name + '/temp.s'
    obj_path = obj_path if obj_path else random_tmp_dir.name + '/temp.o'
    out_path = out_path if out_path else random_tmp_dir.name + '/temp'

    with open(asm_path, 'w') as f:
        f.write('\n'.join(assembly))

    assemble(asm_path, obj_path)
    link(obj_path, out_path)
    
    EXECUTION_MODE = out_path == random_tmp_dir.name + '/temp'
    if EXECUTION_MODE:
        os.system(out_path)


def compile_run(codegen: Codegen, code: str) -> tuple[subprocess.CompletedProcess, str]:
    '''
    Compiles the code and runs the executable.
    Returns the output of the executable and the path to the executable.
    '''
    out_asm = 'tmp/tmp.s'
    out_obj = 'tmp/tmp.o'
    out_exe = 'tmp/tmp'
    
    compile(codegen, code, out_asm, out_obj, out_exe)
    
    # run the executable and return the output
    output = subprocess.run([out_exe], capture_output=True, shell=True, text=True)
    
    return output, out_exe