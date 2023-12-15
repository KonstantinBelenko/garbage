'''
    Runs assembly files
    
    Usage:
        python3 run.py <filepath>
'''

from shared_utils import assemble, link
from utils import args_filepath
import os

if __name__ == "__main__":
    
    filepath, filepath_no_exp = args_filepath()
    assemble(filepath, filepath_no_exp + '.o')
    link(filepath_no_exp + '.o', filepath_no_exp)
    
    os.system(filepath_no_exp)