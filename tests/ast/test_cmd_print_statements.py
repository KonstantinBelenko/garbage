from src.shared_utils import verify

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
    
    verify('_print((5 * 5));', {
        "type": "Program",
        "body": [
            {
                "type": "CmdPrintStatement",
                "body": {
                    "type": "NumericLiteral",
                    "value": 25
                }
            }
        ]
    }, 'print((5 * 5))', optimize=True)
    
    verify('''
        let x = 55;
        _print(x);
        ''', {
            "type": "Program",
            "body": [
                {
                    "type": "VariableDeclaration",
                    "declarations": [
                        {
                            "type": "VariableDeclarator",
                            "id": {
                                "type": "Identifier",
                                "name": "x"
                            },
                            "init": {
                                "type": "NumericLiteral",
                                "value": 55
                            }
                        }
                    ]
                },
                {
                    "type": "CmdPrintStatement",
                    "body": {
                        "type": "Identifier",
                        "name": "x"
                    }
                }
            ]
        }, 'let x = 55; print(x)', optimize=True)