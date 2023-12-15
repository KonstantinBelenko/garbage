from shared_utils import verify

def test():
    
    print('Running test_statement_list.py')
    
    # statement list 
    verify(
        '''
            "Hello World!";
            42;
            'Hello World!';
            32;
        ''',
    {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'StringLiteral',
                    'value': 'Hello World!'
                }
            },
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'NumericLiteral',
                    'value': 42
                }
            },
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'StringLiteral',
                    'value': 'Hello World!'
                }
            },
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'NumericLiteral',
                    'value': 32
                }
            },
        ]
    }, 'Statement List')