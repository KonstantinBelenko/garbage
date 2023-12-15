from src.utils import args_filepath, args_compile_flags
from src.shared_utils import assemble, link

from src.ast_parser import Parser
from src.codegen import CodeGenerator
import tempfile
import os

def main():
    filepath, fileoath_no_ext = args_filepath()
    save_assembly, save_obj, save_output = args_compile_flags()

    parser = Parser()
    codegen = CodeGenerator()
    
    source_code = None
    target_asm = None
    with open(filepath) as f:
        source_code = f.read()

    ast = parser.parse(source_code)
    assembly = codegen.generate(ast)

    random_tmp_dir = tempfile.TemporaryDirectory()

    filename_assembly = fileoath_no_ext + '.s' if save_assembly else random_tmp_dir.name + '/temp.s'
    filename_object = fileoath_no_ext + '.o'if save_obj else random_tmp_dir.name + '/temp.o'
    filename_executable = fileoath_no_ext if save_output else random_tmp_dir.name + '/temp.out'

    with open(filename_assembly, 'w') as f:
        f.write(assembly)

    assemble(filename_assembly, filename_object)
    link(filename_object, filename_executable)
    
    os.system(filename_executable)
    


if __name__ == '__main__':
    main()