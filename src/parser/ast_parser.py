from src.tokenizer import Tokenizer, Token
from enum import Enum

class NodeType(Enum):
    PROGRAM = 'Program'
    STATEMENT_LIST = 'StatementList'
    STATEMENT = 'Statement'
    EXPRESSION_STATEMENT = 'ExpressionStatement'
    CMD_PRINT_STATEMENT = 'CmdPrintStatement'
    BLOCK_STATEMENT = 'BlockStatement'
    EMPTY_STATEMENT = 'EmptyStatement'
    VARIABLE_DECLARATION = 'VariableDeclaration'
    VARIABLE_STATEMENT = 'VariableStatement'
    ASSIGNMENT_EXPRESSION = 'AssignmentExpression'
    IDENTIFIER = 'Identifier'
    BINARY_EXPRESSION = 'BinaryExpression'
    NUMERIC_LITERAL = 'NumericLiteral'
    STRING_LITERAL = 'StringLiteral'
    
    def __eq__(self, other):
        if not isinstance(other, NodeType):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value
    
    def all():
        return list(map(lambda c: c.value, NodeType))


class ASTParser:
    
    def __init__(self) -> None:
        self.builders = {
            'ParseMultiplicativeExpression': self.ParseMultiplicativeExpression,
            'ParsePrimaryExpression': self.ParsePrimaryExpression,
        }
    
    def parse(self, string) -> dict:
        self.string = string
        self.tokenizer = Tokenizer(string)
        self.lookahead = self.tokenizer.get_next_token()
        
        program = self.ParseProgram()
        program = self.collapse_static_expressions(program)
        
        return program
    
    def ParseProgram(self) -> dict:
        '''
        Program
            | StatementList
            ;
        '''
        return {
            'type': NodeType.PROGRAM,
            'body': self.ParseStatementList()
        }
        
    def ParseStatementList(self, stop_lookahead=None) -> list[dict]:
        '''
        StatementList
            | Statement
            | StatementList Statement
            ;
        '''
        statement_list = [self.ParseStatement()]
        
        while self.lookahead is not None and self.lookahead.type is not stop_lookahead:
            statement_list.append( self.ParseStatement() )
        
        return statement_list
        
    def ParseStatement(self) -> dict:
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
            return self.ParseEmptyStatement()
        elif self.lookahead.type == '{':
            return self.ParseBlockStatement()
        elif self.lookahead.type == 'LET':
            return self.ParseVariableStatement()
        elif self.lookahead.type == '_PRINT':
            return self.ParseCmdPrintStatement()
        else:
            return self.ParseExpressionStatement()
    
    def ParseCmdPrintStatement(self) -> dict:
        '''
        CmdPrintStatement
            | example: _print("hello");
            | '_print' ( StringLiteral ) ';'
            ;
        '''
        self.eat('_PRINT')
        self.eat('(')
        expression = self.ParseExpression()
        self.eat(')')
        self.eat(';')
        
        return {
            'type': NodeType.CMD_PRINT_STATEMENT,
            'body': expression
        }

    
    def ParseVariableStatement(self) -> dict:
        '''
        VariableStatement
            | 'let' VariableDeclarationList ';'
            ;
        '''
        self.eat('LET')
        declarations = self.ParseVariableDeclarationList()
        self.eat(';')
        
        return {
            'type': NodeType.VARIABLE_STATEMENT,
            'declarations': declarations
        }
    
    def ParseVariableDeclarationList(self) -> list[dict]:
        '''
        VariableDeclarationList
            | VariableDeclaration
            | VariableDeclarationList ',' VariableDeclaration
            ;
        '''
        declarations = [self.ParseVariableDeclaration()]
        
        while self.lookahead.type == ',':
            self.eat(',')
            declarations.append( self.ParseVariableDeclaration() )
        
        return declarations
    
    def ParseVariableDeclaration(self) -> dict:
        '''
        VariableDeclaration
            | Identifier
            | Identifier '=' Expression
            ;
        '''
        identifier = self.ParseIdentifier()

        init = None        
        if self.lookahead.type != ';' and self.lookahead.type != ',':
            init = self.ParseVariableInitializer()

        return {
            'type': NodeType.VARIABLE_DECLARATION,
            'id': identifier,
            'init': init,
        }            
    
    def ParseVariableInitializer(self) -> dict:
        '''
        VariableInitializer
            | '=' Expression
            ;
        '''
        self.eat('SIMPLE_ASSIGN')
        return self.ParseAssignmentExpression()
    
    def ParseEmptyStatement(self) -> dict:
        '''
        EmptyStatement
            | ';'
            ;
        '''
        self.eat(';')
        return { 'type': NodeType.EMPTY_STATEMENT }
    
    def ParseExpressionStatement(self) ->  dict:
        '''
        ExpressionStatement
            | Expression
            ;
        '''
        
        expression = self.ParseExpression()
        self.eat(';')
        return {
            'type': NodeType.EXPRESSION_STATEMENT,
            'body': expression
        }
        
    def ParseBlockStatement(self) -> dict:
        '''
        BlockStatement
            | '{' OptStatementList '}'
            ;
        '''
        self.eat('{')
        
        body = None
        if self.lookahead.type != '}':
            body = self.ParseStatementList(stop_lookahead='}')
        else:
            body = []
        
        self.eat('}')
        
        return {
            'type': NodeType.BLOCK_STATEMENT,
            'body': body
        }
        
    def ParseExpression(self) -> dict:
        '''
        Expression
            | Literal
            ;
        '''
        
        return self.ParseAssignmentExpression()
    
    def ParseAssignmentExpression(self) -> dict:
        '''
        AssignmentExpression
            | AdditiveExpression
            | LeftHandSideExpression AssignmentOperator AssignmentExpression
            ;
        '''
        left = self.ParseAdditiveExpression()
        if not self._isAssignmentOperator(self.lookahead):
            return left
        
        return {
            'type': NodeType.ASSIGNMENT_EXPRESSION,
            'operator': self.ParseAssignmentOperator().value,
            'left': self._checkValidAssignmentTarget(left),
            'right': self.ParseAssignmentExpression()
        }
    
    def ParseLeftHandSideExpression(self) -> dict:
        '''
        LeftHandSideExpression
            | Identifier
            ;
        '''
        return self.ParseIdentifier()
    
    def ParseIdentifier(self) -> dict:
        '''
        Identifier
            | IDENTIFIER
            ;
        '''
        token = self.eat('IDENTIFIER')
        return {
            'type': NodeType.IDENTIFIER,
            'name': token.value
        }
        
    def _checkValidAssignmentTarget(self, expression: dict) -> dict:
        if expression['type'] == NodeType.IDENTIFIER:
            return expression
        else:
            raise Exception('Invalid left-hand side in assignment')
    
    def _isAssignmentOperator(self, token: Token) -> bool:
        return token.type == 'SIMPLE_ASSIGN' or token.type == 'COMPLEX_ASSIGN'
    
    def ParseAssignmentOperator(self) -> Token:
        '''
        AssignmentOperator
            | '='
            | '*='
            | '/='
            | '+='
            | '-='
            ;
        '''
        if self.lookahead.type == 'SIMPLE_ASSIGN':
            return self.eat('SIMPLE_ASSIGN')
        return self.eat('COMPLEX_ASSIGN')
    
    def ParseAdditiveExpression(self) -> dict:
        '''
        AdditiveExpression
            | Literal
            | AdditiveExpression ADDITIVE_OPERATOR Literal
            ;
        '''
        return self._BinaryExpression('ParseMultiplicativeExpression', 'ADDITIVE_OPERATOR')

    def _BinaryExpression(self, builderName, operatorToken):
        left = self.builders[builderName]()
        while self.lookahead.type == operatorToken:
            operator = self.eat(operatorToken).value
            right = self.builders[builderName]()
            
            left = {
                'type': NodeType.BINARY_EXPRESSION,
                'operator': operator,
                'left': left,
                'right': right
            }
        
        return left

    def ParseMultiplicativeExpression(self) -> dict:
        '''
        MultiplicativeExpression
            | Literal
            | MultiplicativeExpression MULTIPLICATIVE_OPERATOR Literal
            ;
        '''
        return self._BinaryExpression('ParsePrimaryExpression', 'MULTIPLICATIVE_OPERATOR')
    
    def ParsePrimaryExpression(self) -> dict:
        '''
        PrimaryExpression
            | Literal
            | ParenthesizedExpression
            | LeftHandSideExpression
            ;
        '''
        
        if self._isLiteral(self.lookahead.type):
            return self.ParseLiteral()
        
        if self.lookahead.type == '(':
            return self.ParseParenthesizedExpression()
        else:
            return self.ParseLeftHandSideExpression()
    
    def _isLiteral(self, token: Token) -> bool:
        return token == 'NUMBER' or token == 'STRING'
    
    def ParseParenthesizedExpression(self) -> dict:
        '''
        ParenthesizedExpression
            | '(' Expression ')'
            ;
        '''
        self.eat('(')
        expression = self.ParseExpression()
        self.eat(')')
        
        return expression
    
    def ParseLiteral(self) -> dict:
        '''
        Literal
            | NumericLiteral
            | StringLiteral
            ;
        '''
        
        if self.lookahead.type == 'NUMBER':
            return self.ParseNumericLiteral()
        elif self.lookahead.type == 'STRING':
            return self.ParseStringLiteral()
        else:
            raise Exception(f'Unexpected token {self.lookahead.type}')
        
    def ParseStringLiteral(self) -> dict:
        '''
        StringLiteral
            | '"' [a-zA-Z0-9]* '"'
            ;
        '''
        token: Token = self.eat('STRING')
        return {
            'type': NodeType.STRING_LITERAL,
            'value': token.value[1:-1]
        }
        
    def ParseNumericLiteral(self) -> dict:
        '''
        NumericLiteral
            | [0-9]+
            ;
        '''
        
        token: Token = self.eat('NUMBER')
        return {
            'type': NodeType.NUMERIC_LITERAL,
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
                node[key] = [ASTParser.collapse_static_expressions(item) for item in value]
            elif isinstance(value, dict):
                node[key] = ASTParser.collapse_static_expressions(value)

        if ASTParser.is_static_expression(node):
            return ASTParser.evaluate_static_expression(node)
        
        return node
    
    @staticmethod
    def is_static_expression(node: dict) -> bool:
        if node['type'] != NodeType.BINARY_EXPRESSION:
            return False
        if not isinstance(node['left'], dict) or not isinstance(node['right'], dict):
            return False
        return node['left']['type'] == NodeType.NUMERIC_LITERAL and node['right']['type'] == NodeType.NUMERIC_LITERAL
    
    @staticmethod
    def evaluate_static_expression(node: dict) -> dict:
        left_value = node['left']['value']
        right_value = node['right']['value']
        operator = node['operator']
        result = ASTParser.apply_operator(left_value, right_value, operator)
        return {
            'type': NodeType.NUMERIC_LITERAL,
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