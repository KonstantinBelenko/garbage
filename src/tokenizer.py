import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __json__(self):
        return {
            'type': self.type,
            'value': self.value
        }

class Tokenizer:
    
    spec = [
        # -----------------
        # Whitespace:
        (None, r'^\s+'),
        (None, r'^\/\/.*'),
        (None, r'^\/\*[\s\S]*?\*\/'),
        (None, r'^#.*'),
        
        # -----------------
        # Keywords:
        ('LET', r'^\blet\b'),
        
        # -----------------
        # Hardcode commands:
        ('_PRINT', r'^_print'),
        
        # -----------------
        # Numbers:
        ('NUMBER', r'^[0-9]+(\.[0-9]+)?'),
        
        # -----------------
        # Strings:
        ('STRING', r'^"[^"]*"'),  # Matches any character except " between double quotes
        ('STRING', r'^\'[^\']*\''),  # Matches any character except ' between single quotes
        
        # -----------------
        # Symbols:
        (';', r'^;'),
        ('{', r'^{'),
        ('}', r'^}'),
        ('(', r'^\('),
        (')', r'^\)'),
        (',', r'^,'),
        
        # -----------------
        # Identifiers:
        ('IDENTIFIER', r'^\w+'),
        
        # -----------------
        # Assignment: =, *=, /=, +=, -=
        ('SIMPLE_ASSIGN', r'^='),
        ('COMPLEX_ASSIGN', r'^[\*\+\-\/]='),
        
        
        # -----------------
        # Math:
        ('ADDITIVE_OPERATOR', r'^\+'),
        ('ADDITIVE_OPERATOR', r'^\-'),
        ('MULTIPLICATIVE_OPERATOR', r'^\*'),
        ('MULTIPLICATIVE_OPERATOR', r'^\/'),
    ]
    
    def __init__(self, text):
        self.text = text
        self.cursor = 0
        
    def has_more_tokens(self):
        return self.cursor < len(self.text)
        
    def get_next_token(self):
        if not self.has_more_tokens():
            return None
        
        char: str = self.text[self.cursor]
        for type, regex in Tokenizer.spec:
            matched = self._match(regex, self.text[self.cursor:])
            
            if matched is None:
                continue
            
            if type is None:
                return self.get_next_token()
            
            return Token(type, matched)
        
        raise Exception(f'Unexpected character {char}')
    
    def _match(self, regexp, text):
        matched = re.match(regexp, text)
        if matched:
            self.cursor += len(matched.group(0))
            return matched.group(0)
        else:
            return None