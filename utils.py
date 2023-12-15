from shared_types import Result, Ok, Err
import argparse
import sys
import os

def args_filepath() -> tuple[str, str]:
    if len(sys.argv) < 2:
        return Exception("Please provide a filepath")
    
    path = sys.argv[1]
    filepath_no_ext, _ = os.path.splitext(path)
    
    return path, filepath_no_ext

def args_compile_flags() -> tuple[str, str]:
    '''
    returns = tuple[ -s assembly | bool, -o output | bool ]
    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str)
    parser.add_argument('-s', '--assembly', action='store_true', default=False, required=False)
    parser.add_argument('-o', '--output', action='store_true', default=False, required=False)
    parser.add_argument('-so', '--saveobj', action='store_true', default=False, required=False)
    args = parser.parse_args()
    
    return args.assembly, args.saveobj, args.output
