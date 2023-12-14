from shared_utils import verify

def test():
    print('Running test_math.py')
    
    verify('2 + 2;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'BinaryExpression',
                    'operator': '+',
                    'left': {
                        'type': 'NumericLiteral',
                        'value': 2
                    },
                    'right': {
                        'type': 'NumericLiteral',
                        'value': 2
                    }
                }
            }
        ]
    }, 'Addition')
    
    verify('3 + 2 - 2;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'BinaryExpression',
                    'operator': '-',
                    'left': {
                        'type': 'BinaryExpression',
                        'operator': '+',
                        'left': {
                            'type': 'NumericLiteral',
                            'value': 3
                        },
                        'right': {
                            'type': 'NumericLiteral',
                            'value': 2
                        }
                    },
                    'right': {
                        'type': 'NumericLiteral',
                        'value': 2
                    }
                }
            }
        ]
    }, 'Subtraction')
    
    verify('2 * 2;', {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'BinaryExpression',
                    'operator': '*',
                    'left': {
                        'type': 'NumericLiteral',
                        'value': 2
                    },
                    'right': {
                        'type': 'NumericLiteral',
                        'value': 2
                    }
                }
            }
        ]
    }, 'Multiplication')
    
    verify("2 + 2 * 2;", {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'BinaryExpression',
                    'operator': '+',
                    'left': {
                        'type': 'NumericLiteral',
                        'value': 2
                    },
                    'right': {
                        'type': 'BinaryExpression',
                        'operator': '*',
                        'left': {
                            'type': 'NumericLiteral',
                            'value': 2
                        },
                        'right': {
                            'type': 'NumericLiteral',
                            'value': 2
                        }
                    }
                }
            }
        ]
    }, 'Multiplication and Addition')
    
    verify("(2 + 2) * 2;", {
        'type': 'Program',
        'body': [
            {
                'type': 'ExpressionStatement',
                'body': {
                    'type': 'BinaryExpression',
                    'operator': '*',
                    'left': {
                        'type': 'BinaryExpression',
                        'operator': '+',
                        'left': {
                            'type': 'NumericLiteral',
                            'value': 2
                        },
                        'right': {
                            'type': 'NumericLiteral',
                            'value': 2
                        }
                    },
                    'right': {
                        'type': 'NumericLiteral',
                        'value': 2
                    }
                }
            }
        ]
    }, 'Parentheses')