from src.shared_utils import verify

def test():
    
    print('Running test_block_statements.py')
    
    verify('''
        
        {
            42;
            
            "Hello";
        }
        ''', {   
        'type': 'Program',
        'body': [
            {
                'type': 'BlockStatement',
                'body': [
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
                            'value': 'Hello'
                        }
                    }
                ]
            }
        ]
    }, 'BlockStatement')
    
    verify('{}', {
        'type': 'Program',
        'body': [
            {
                'type': 'BlockStatement',
                'body': []
            }
        ]
    }, 'Empty BlockStatement')
    
    verify('''
        {
            42;
            {
                'hello';
            }
        }
        ''', {
        'type': 'Program',
        'body': [
            {
                'type': 'BlockStatement',
                'body': [
                    {
                        'type': 'ExpressionStatement',
                        'body': {
                            'type': 'NumericLiteral',
                            'value': 42
                        }
                    },
                    {
                        'type': 'BlockStatement',
                        'body': [
                            {
                                'type': 'ExpressionStatement',
                                'body': {
                                    'type': 'StringLiteral',
                                    'value': 'hello'
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }, 'Nested BlockStatement')