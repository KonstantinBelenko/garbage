from shared_utils import verify

def test():
    
    print('Running test_cmd_print_statements.py')
    
    verify('_print("Hello, world!");', {
        "type": "Program",
        "body": [
            {
                "type": "CmdPrintStatement",
                "body": {
                    "type": "StringLiteral",
                    "value": "Hello, world!"
                }
            }
        ]
    }, 'print("Hello, world!")', optimize=True)
    
    verify('_print(42);', {
        "type": "Program",
        "body": [
            {
                "type": "CmdPrintStatement",
                "body": {
                    "type": "NumericLiteral",
                    "value": 42
                }
            }
        ]
    }, 'print(42)', optimize=True)
    
    verify('_print(5 + 15);', {
        "type": "Program",
        "body": [
            {
                "type": "CmdPrintStatement",
                "body": {
                    "type": "NumericLiteral",
                    "value": 20
                }
            }
        ]
    }, 'print(5 + 15)', optimize=True)
    