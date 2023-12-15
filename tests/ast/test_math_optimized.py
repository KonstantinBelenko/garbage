from shared_utils import verify

def test():
    print('Running test_math_optimized.py')
    
    verify('2 + 2;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'NumericLiteral',
                    'value': 4
                }
            }
        ]
    }, 'Addition optimized', optimize=True)
    
    verify('3 + 2 - 2;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'NumericLiteral',
                    'value': 3
                }
            }
        ]
    }, 'Subtraction optimized', optimize=True)
    
    verify('2 * 2;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'NumericLiteral',
                    'value': 4
                }
            }
        ]
    }, 'Multiplication optimized', optimize=True)
    
    verify("2 + 2 * 2;", {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'NumericLiteral',
                    'value': 6
                }
            }
        ]
    }, 'Multiplication and Addition optimized', optimize=True)
    
    verify("(2 + 2) * 2;", {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'NumericLiteral',
                    'value': 8
                }
            }
        ]
    }, 'Parentheses optimized', optimize=True)