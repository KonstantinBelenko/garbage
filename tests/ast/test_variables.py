from shared_utils import verify

def test():
    
    print('Running test_variables.py')
    
    verify('let x = 42;', {
        'type': 'Program',
        'body': [
            {
                'type': 'VariableDeclaration',
                'declarations': [
                    {
                        'type': 'VariableDeclarator',
                        'id': {
                            'type': 'Identifier',
                            'name': 'x'
                        },
                        'init': {
                            'type': 'NumericLiteral',
                            'value': 42
                        }
                    }
                ]
            }
        ]
    }, 'VariableDeclaration')
    
    verify('''
        let x = 42;
        let y = 42;
        let c = x + y + x;
    ''',  {
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
                            "value": 42
                        }
                    }
                ]
            },
            {
                "type": "VariableDeclaration",
                "declarations": [
                    {
                        "type": "VariableDeclarator",
                        "id": {
                            "type": "Identifier",
                            "name": "y"
                        },
                        "init": {
                            "type": "NumericLiteral",
                            "value": 42
                        }
                    }
                ]
            },
            {
                "type": "VariableDeclaration",
                "declarations": [
                    {
                        "type": "VariableDeclarator",
                        "id": {
                            "type": "Identifier",
                            "name": "c"
                        },
                        "init": {
                            "type": "BinaryExpression",
                            "operator": "+",
                            "left": {
                                "type": "BinaryExpression",
                                "operator": "+",
                                "left": {
                                    "type": "Identifier",
                                    "name": "x"
                                },
                                "right": {
                                    "type": "Identifier",
                                    "name": "y"
                                }
                            },
                            "right": {
                                "type": "Identifier",
                                "name": "x"
                            }
                        }
                    }
                ]
            }
        ]
    }, 'Multiple Variable Declarations')
    
    verify('let x, y;', {
        'type': 'Program',
        'body': [
            {
                'type': 'VariableDeclaration',
                'declarations': [
                    {
                        'type': 'VariableDeclarator',
                        'id': {
                            'type': 'Identifier',
                            'name': 'x'
                        },
                        'init': None
                    },
                    {
                        'type': 'VariableDeclarator',
                        'id': {
                            'type': 'Identifier',
                            'name': 'y'
                        },
                        'init': None
                    }
                ]
            }
        ]
    }, 'VariableDeclaration with multiple declarations')
    
    verify('let x, y = 42;', {
        'type': 'Program',
        'body': [
            {
                'type': 'VariableDeclaration',
                'declarations': [
                    {
                        'type': 'VariableDeclarator',
                        'id': {
                            'type': 'Identifier',
                            'name': 'x'
                        },
                        'init': None, 
                    },
                    {
                        'type': 'VariableDeclarator',
                        'id': {
                            'type': 'Identifier',
                            'name': 'y'
                        },
                        'init': {
                            'type': 'NumericLiteral',
                            'value': 42
                        }
                    }
                ]
            }
        ]
    }, 'VariableDeclaration with multiple declarations and one assignment')
    
    verify('''
        let x = 5;
        let y = 5;
        let c = x + y;    
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
                            "value": 5
                        }
                    }
                ]
            },
            {
                "type": "VariableDeclaration",
                "declarations": [
                    {
                        "type": "VariableDeclarator",
                        "id": {
                            "type": "Identifier",
                            "name": "y"
                        },
                        "init": {
                            "type": "NumericLiteral",
                            "value": 5
                        }
                    }
                ]
            },
            {
                "type": "VariableDeclaration",
                "declarations": [
                    {
                        "type": "VariableDeclarator",
                        "id": {
                            "type": "Identifier",
                            "name": "c"
                        },
                        "init": {
                            "type": "BinaryExpression",
                            "operator": "+",
                            "left": {
                                "type": "Identifier",
                                "name": "x"
                            },
                            "right": {
                                "type": "Identifier",
                                "name": "y"
                            }
                        }
                    }
                ]
            }
        ]
    }, 'VariableDeclaration with multiple declarations and multiple assignments')