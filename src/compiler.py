from src.parser import ASTParser
from src.codegen import CodeGenerator
from src.shared_utils import assemble, link

from typing import Optional
import tempfile
    
def compile(code: str, asm_path: Optional[str] = None, obj_path: Optional[str] = None, out_path: Optional[str] = None):

    parser = ASTParser()
    codegen = CodeGenerator()
    
    ast = parser.parse(code)
    assembly: list[str] = codegen.generate(ast)

    random_tmp_dir = tempfile.TemporaryDirectory()
    asm_path = asm_path if asm_path else random_tmp_dir.name + '/temp.s'
    obj_path = obj_path if obj_path else random_tmp_dir.name + '/temp.o'
    out_path = out_path if out_path else random_tmp_dir.name + '/temp'

    with open(asm_path, 'w') as f:
        f.write('\n'.join(assembly))

    assemble(asm_path, obj_path)
    link(obj_path, out_path)

def compile_test(code: str):
    compile(code, 'temp.s', None, 'temp.out')