from src.utils import args_parse, get_file_paths
from src.shared_utils import assemble, link

from src.compiler import compile

def main():
    args = args_parse()
    filepath, filepath_no_ext = get_file_paths(args.filepath)

    asm_path = filepath_no_ext + '.s' if args.assembly else None
    obj_path = filepath_no_ext + '.o' if args.saveobj else None
    out_path = args.output

    with open(filepath, 'r') as f:
        code = f.read()

    compile(code, asm_path, obj_path, out_path)


if __name__ == '__main__':
    main()