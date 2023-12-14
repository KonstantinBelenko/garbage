from utils import args_filepath

def main():
    filepath = args_filepath().expect("Please provide a filepath")
    

if __name__ == '__main__':
    main()