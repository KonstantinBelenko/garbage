import subprocess


def assemble(file_in: str, file_out: str):
    compile_result = subprocess.run(['as', '-g', file_in, '-o', file_out], capture_output=True)
    if compile_result.returncode != 0:
        print("Error compiling:\n", compile_result.stderr.decode('utf-8'))
        assert compile_result.returncode == 0

def link(file_in: str, file_out: str):
    
    sdk_path_result = subprocess.run(['xcrun', '--sdk', 'macosx', '--show-sdk-path'], capture_output=True, text=True)
    if sdk_path_result.returncode != 0:
        print("Error getting SDK path:\n", sdk_path_result.stderr)
        assert sdk_path_result.returncode == 0
    sdk_path = sdk_path_result.stdout.strip()

    link_command = ['ld', file_in, '-o', file_out, '-L' + sdk_path + '/usr/lib', '-lSystem', '-e', '_main', '-arch', 'arm64']
    link_result = subprocess.run(link_command, capture_output=True, text=True)
    if link_result.returncode != 0:
        print("Error linking:\n", link_result.stderr)
        assert link_result.returncode == 0