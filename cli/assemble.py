'''
    Runs assembly files
    
    Usage:
        python3 run.py <filepath>
'''

from src.shared_utils import assemble, link
from src.utils import args_parse, get_file_paths

def main():
    args = args_parse()
    filepath, filepath_no_ext = get_file_paths(args.filepath)
    
    assemble(filepath, filepath_no_ext + '.o')
    link(filepath_no_ext + '.o', filepath_no_ext)

if __name__ == "__main__":
    main()