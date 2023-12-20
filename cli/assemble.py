'''
    Runs assembly files
    
    Usage:
        python3 run.py <filepath>
'''

from src.shared_utils import assemble, link
from src.utils import args_filepath

def main():
    filepath, filepath_no_exp = args_filepath()
    assemble(filepath, filepath_no_exp + '.o')
    link(filepath_no_exp + '.o', filepath_no_exp)

if __name__ == "__main__":
    main()