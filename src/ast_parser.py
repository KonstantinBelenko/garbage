from src.tokenizer import Tokenizer, Token
import json


class Parser:
    
    def __init__(self) -> None:
        self.builders = {
            'MultiplicativeExpression': self.MultiplicativeExpression,
            'PrimaryExpression': self.PrimaryExpression,
        }
    
    def parse(self, string) -> dict:
        self.string = string
        self.tokenizer = Tokenizer(string)
        
        self.lookahead = self.tokenizer.get_next_token()
        
        return self.Program()
    
    def parse_optimized(self, string) -> dict:
        self.string = string
        self.tokenizer = Tokenizer(string)
        
        self.lookahead = self.tokenizer.get_next_token()
        
        program = self.Program()
        
        program = self.collapse_static_expressions(program)
        
        return program
    
    def Program(self) -> dict:
        '''
        Program
            | StatementList
            ;
        '''
        return {
            'type': 'Program',
            'body': self.StatementList()
        }
        
    def StatementList(self, stop_lookahead=None) -> list[dict]:
        '''
        StatementList
            | Statement
            | StatementList Statement
            ;
        '''
        statement_list = [self.Statement()]
        
        while self.lookahead is not None and self.lookahead.type is not stop_lookahead:
            statement_list.append( self.Statement() )
        
        return statement_list
        
    def Statement(self) -> dict:
        '''
        Statement
            | ExpressionStatement
            | BlockStatement
            | EmptyStatement
            | VariableStatement
            | CmdPrintStatement
            ;
        '''
        if self.lookahead.type == ';':
            return self.EmptyStatement()
        elif self.lookahead.type == '{':
            return self.BlockStatement()
        elif self.lookahead.type == 'LET':
            return self.VariableStatement()
        elif self.lookahead.type == '_PRINT':
            return self.CmdPrintStatement()
        else:
            return self.ExpressionStatement()
    
    def CmdPrintStatement(self) -> dict:
        '''
        CmdPrintStatement
            | example: _print("hello");
            | '_print' ( StringLiteral ) ';'
            ;
        '''
        self.eat('_PRINT')
        self.eat('(')
        expression = self.Expression()
        self.eat(')')
        self.eat(';')
        
        return {
            'type': 'CmdPrintStatement',
            'body': expression
        }

    
    def VariableStatement(self) -> dict:
        '''
        VariableStatement
            | 'let' VariableDeclarationList ';'
            ;
        '''
        self.eat('LET')
        declarations = self.VariableDeclarationList()
        self.eat(';')
        
        return {
            'type': 'VariableDeclaration',
            'declarations': declarations
        }
    
    def VariableDeclarationList(self) -> list[dict]:
        '''
        VariableDeclarationList
            | VariableDeclaration
            | VariableDeclarationList ',' VariableDeclaration
            ;
        '''
        declarations = [self.VariableDeclaration()]
        
        while self.lookahead.type == ',':
            self.eat(',')
            declarations.append( self.VariableDeclaration() )
        
        return declarations
    
    def VariableDeclaration(self) -> dict:
        '''
        VariableDeclaration
            | Identifier
            | Identifier '=' Expression
            ;
        '''
        identifier = self.Identifier()

        init = None        
        if self.lookahead.type != ';' and self.lookahead.type != ',':
            init = self.VariableInitializer()

        return {
            'type': 'VariableDeclarator',
            'id': identifier,
            'init': init,
        }            
    
    def VariableInitializer(self) -> dict:
        '''
        VariableInitializer
            | '=' Expression
            ;
        '''
        self.eat('SIMPLE_ASSIGN')
        return self.AssignmentExpression()
    
    def EmptyStatement(self) -> dict:
        '''
        EmptyStatement
            | ';'
            ;
        '''
        self.eat(';')
        return { 'type': 'EmptyStatement' }
    
    def ExpressionStatement(self) ->  dict:
        '''
        ExpressionStatement
            | Expression
            ;
        '''
        
        expression = self.Expression()
        self.eat(';')
        return {
            'type': 'ExpressionStatement',
            'body': expression
        }
        
    def BlockStatement(self) -> dict:
        '''
        BlockStatement
            | '{' OptStatementList '}'
            ;
        '''
        self.eat('{')
        
        body = None
        if self.lookahead.type != '}':
            body = self.StatementList(stop_lookahead='}')
        else:
            body = []
        
        self.eat('}')
        
        return {
            'type': 'BlockStatement',
            'body': body
        }
        
    def Expression(self) -> dict:
        '''
        Expression
            | Literal
            ;
        '''
        
        return self.AssignmentExpression()
        # return self.AdditiveExpression()
    
    def AssignmentExpression(self) -> dict:
        '''
        AssignmentExpression
            | AdditiveExpression
            | LeftHandSideExpression AssignmentOperator AssignmentExpression
            ;
        '''
        left = self.AdditiveExpression()
        if not self._isAssignmentOperator(self.lookahead):
            return left
        
        return {
            'type': 'AssignmentExpression',
            'operator': self.AssignmentOperator().value,
            'left': self._checkValidAssignmentTarget(left),
            'right': self.AssignmentExpression()
        }
    
    def LeftHandSideExpression(self) -> dict:
        '''
        LeftHandSideExpression
            | Identifier
            ;
        '''
        return self.Identifier()
    
    def Identifier(self) -> dict:
        '''
        Identifier
            | IDENTIFIER
            ;
        '''
        token = self.eat('IDENTIFIER')
        return {
            'type': 'Identifier',
            'name': token.value
        }
        
    def _checkValidAssignmentTarget(self, expression: dict) -> dict:
        if expression['type'] == 'Identifier':
            return expression
        else:
            raise Exception('Invalid left-hand side in assignment')
    
    def _isAssignmentOperator(self, token: Token) -> bool:
        return token.type == 'SIMPLE_ASSIGN' or token.type == 'COMPLEX_ASSIGN'
    
    def AssignmentOperator(self) -> Token:
        '''
        AssignmentOperator
            | '='
            | '*='
            | '/='
            | '+='
            | '-='
            ;
        '''
        token = self.lookahead
        if self.lookahead.type == 'SIMPLE_ASSIGN':
            return self.eat('SIMPLE_ASSIGN')
        return self.eat('COMPLEX_ASSIGN')
    
    def AdditiveExpression(self) -> dict:
        '''
        AdditiveExpression
            | Literal
            | AdditiveExpression ADDITIVE_OPERATOR Literal
            ;
        '''
        return self._BinaryExpression('MultiplicativeExpression', 'ADDITIVE_OPERATOR')

    def _BinaryExpression(self, builderName, operatorToken):
        left = self.builders[builderName]()
        while self.lookahead.type == operatorToken:
            operator = self.eat(operatorToken).value
            right = self.builders[builderName]()
            
            left = {
                'type': 'BinaryExpression',
                'operator': operator,
                'left': left,
                'right': right
            }
        
        return left

    def MultiplicativeExpression(self) -> dict:
        '''
        MultiplicativeExpression
            | Literal
            | MultiplicativeExpression MULTIPLICATIVE_OPERATOR Literal
            ;
        '''
        return self._BinaryExpression('PrimaryExpression', 'MULTIPLICATIVE_OPERATOR')
    
    def PrimaryExpression(self) -> dict:
        '''
        PrimaryExpression
            | Literal
            | ParenthesizedExpression
            | LeftHandSideExpression
            ;
        '''
        
        if self._isLiteral(self.lookahead.type):
            return self.Literal()
        
        if self.lookahead.type == '(':
            return self.ParenthesizedExpression()
        else:
            return self.LeftHandSideExpression()
    
    def _isLiteral(self, token: Token) -> bool:
        return token == 'NUMBER' or token == 'STRING'
    
    def ParenthesizedExpression(self) -> dict:
        '''
        ParenthesizedExpression
            | '(' Expression ')'
            ;
        '''
        self.eat('(')
        expression = self.Expression()
        self.eat(')')
        
        return expression
    
    def Literal(self) -> dict:
        '''
        Literal
            | NumericLiteral
            | StringLiteral
            ;
        '''
        
        if self.lookahead.type == 'NUMBER':
            return self.NumericLiteral()
        elif self.lookahead.type == 'STRING':
            return self.StringLiteral()
        else:
            raise Exception(f'Unexpected token {self.lookahead.type}')
        
    def StringLiteral(self) -> dict:
        '''
        StringLiteral
            | '"' [a-zA-Z0-9]* '"'
            ;
        '''
        token: Token = self.eat('STRING')
        return {
            'type': 'StringLiteral',
            'value': token.value[1:-1]
        }
        
    def NumericLiteral(self) -> dict:
        '''
        NumericLiteral
            | [0-9]+
            ;
        '''
        
        token: Token = self.eat('NUMBER')
        return {
            'type': 'NumericLiteral',
            'value': int(token.value)
        }
    
    def eat(self, type) -> Token:
        if self.lookahead is None:
            raise Exception('Unexpected end of input, you may be missing a semicolon \";\"')
        
        token = self.lookahead
        
        if token.type != type:
            raise Exception(f'Unexpected token {token.type}')
        
        self.lookahead = self.tokenizer.get_next_token()
        
        return token
    
    
    @staticmethod
    def collapse_static_expressions(node):
        if not isinstance(node, dict):
            return node

        for key, value in node.items():
            if isinstance(value, list):
                node[key] = [Parser.collapse_static_expressions(item) for item in value]
            elif isinstance(value, dict):
                node[key] = Parser.collapse_static_expressions(value)

        if Parser.is_static_expression(node):
            return Parser.evaluate_static_expression(node)
        
        return node
    
    @staticmethod
    def is_static_expression(node: dict) -> bool:
        if node['type'] != 'BinaryExpression':
            return False
        if not isinstance(node['left'], dict) or not isinstance(node['right'], dict):
            return False
        return node['left']['type'] == 'NumericLiteral' and node['right']['type'] == 'NumericLiteral'
    
    @staticmethod
    def evaluate_static_expression(node: dict) -> dict:
        left_value = node['left']['value']
        right_value = node['right']['value']
        operator = node['operator']
        result = Parser.apply_operator(left_value, right_value, operator)
        return {
            'type': 'NumericLiteral',
            'value': result
        }
    
    @staticmethod
    def apply_operator(left: int, right: int, operator: str) -> int:
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left // right  # Integer division
        else:
            raise Exception(f'Unknown operator: {operator}')