from src.shared_utils import verify

def test():
    
    print('Running test_empty_statements.py')
    
    verify(';', {
        'type': 'Program',
        'body': [
            {
                'type': 'EmptyStatement',
            }
        ]
    }, 'EmptyStatement')
    
    verify(';;', {
        'type': 'Program',
        'body': [
            {
                'type': 'EmptyStatement',
            },
            {
                'type': 'EmptyStatement',
            }
        ]
    }, 'Multiple EmptyStatements')