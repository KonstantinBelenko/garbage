from src.shared_utils import verify

def test():
    
    print('Running test_literals.py')
    
    verify('42;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'NumericLiteral',
                    'value': 42
                }   
            }
        ]
    }, 'NumericLiteral')
    
    verify('"Hello";', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'StringLiteral',
                    'value': 'Hello'
                }
            }
        ]
    }, 'StringLiteral (double quotes)')
    
    verify('\'Hello\';', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'StringLiteral',
                    'value': 'Hello'
                }
            }
        ]
    }, 'StringLiteral (single quotes)')