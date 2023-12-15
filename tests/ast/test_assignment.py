from src.shared_utils import verify

def test():
    
    print('Running test_assignment.py')
    
    verify('x = 42;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'AssignmentExpression',
                    'operator': '=',
                    'left': {
                        'type': 'Identifier',
                        'name': 'x'
                    },
                    'right': {
                        'type': 'NumericLiteral',
                        'value': 42
                    }
                }
            }
        ]
    }, 'AssignmentExpression')
    
    verify('x = y = 42;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'AssignmentExpression',
                    'operator': '=',
                    'left': {
                        'type': 'Identifier',
                        'name': 'x'
                    },
                    'right': {
                        'type': 'AssignmentExpression',
                        'operator': '=',
                        'left': {
                            'type': 'Identifier',
                            'name': 'y'
                        },
                        'right': {
                            'type': 'NumericLiteral',
                            'value': 42
                        }
                    }
                }
            }
        ]
    }, 'Chained AssignmentExpression')