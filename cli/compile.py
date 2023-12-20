from src.utils import args_filepath, args_compile_flags
from src.shared_utils import assemble, link

from src.compiler import compile

import tempfile
import os

def main():
    filepath, fileoath_no_ext = args_filepath()
    save_assembly, save_obj, save_output = args_compile_flags()

    asm_path = fileoath_no_ext + '.s' if save_assembly else None
    obj_path = fileoath_no_ext + '.o' if save_obj else None
    out_path = fileoath_no_ext if save_output else None

    compile(filepath, asm_path, obj_path, out_path)

    EXECUTION_MODE = not save_output
    if EXECUTION_MODE:
        os.system(f'./{out_path}')


if __name__ == '__main__':
    main()