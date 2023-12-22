import os
import argparse

def get_file_paths(filepath: str) -> tuple[str, str]:
    filepath_no_ext, _ = os.path.splitext(filepath)
    return filepath, filepath_no_ext

def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str, help='Path to the source file')
    parser.add_argument('-s', '--assembly', action='store_true', help='Compile to assembly')
    parser.add_argument('-o', '--output', action='store_true', help='Output file')
    parser.add_argument('-so', '--saveobj', action='store_true', help='Save object file')
    return parser.parse_args()