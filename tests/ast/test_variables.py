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