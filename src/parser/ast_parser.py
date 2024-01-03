from src.tokenizer import Tokenizer, Token
from .ast_node import NT, Node

class ASTParser:
    
    def __init__(self) -> None:
        self.builders = {
            'ParseMultiplicativeExpression': self.ParseMultiplicativeExpression,
            'ParsePrimaryExpression': self.ParsePrimaryExpression,
            'ParseAdditiveExpression': self.ParseAdditiveExpression,
            'ParseRelationalExpression': self.ParseRelationalExpression,
            'ParseEqualityExpression': self.ParseEqualityExpression,
            'ParseUnaryExpression': self.ParseUnaryExpression,
            
            'ParseLogicalANDExpression': self.ParseLogicalANDExpression,
            'ParseLogicalORExpression': self.ParseLogicalORExpression,
        }
        self.optimizer = Optimizer()
    
    def parse(self, string) -> Node:
        self.string = string
        self.tokenizer = Tokenizer(string)
        self.lookahead = self.tokenizer.get_next_token()
        
        program = self.ParseProgram()
        program = self.optimizer.collapse_static_binary_expressions(program)
        
        return program
    
    # def ParseProgram(self) -> dict:
    def ParseProgram(self) -> Node:
        '''
        Program
            | Statement[]
            ;
        '''
        return Node(NT.PROGRAM, children=self.ParseStatementList())
        
    def ParseStatementList(self, stop_lookahead=None) -> list[Node]:
        '''
        StatementList
            | Statement
            | StatementList, Statement
            ;
        '''
        statement_list = [self.ParseStatement()]
        
        while self.lookahead is not None and self.lookahead.type is not stop_lookahead:
            statement_list.append( self.ParseStatement() )
        
        return statement_list
        
    def ParseStatement(self) -> Node:
        '''
        Statement
            | ExpressionStatement
            | BlockStatement
            | EmptyStatement
            | VariableStatement
            | CmdPrintStatement
            | IfStatement
            | IterationStatement
            | FunctionDeclarationStatement
            ;
        '''
        if self.lookahead.type == ';':
            return self.ParseEmptyStatement()
        elif self.lookahead.type == 'IF':
            return self.ParseIfStatement()
        elif self.lookahead.type == '{':
            return self.ParseBlockStatement()
        elif self.lookahead.type == 'LET':
            return self.ParseVariableStatement()
        elif self.lookahead.type == '_PRINT':
            return self.CmdPrintStatement()
        elif self.lookahead.type == 'WHILE' or self.lookahead.type == 'DO' or self.lookahead.type == 'FOR':
            return self.ParseIterationStatement()
        elif self.lookahead.type == 'DEF':
            return self.ParseFunctionDeclarationStatement()
        elif self.lookahead.type == 'RETURN':
            return self.ParseReturnStatement()
        else:
            return self.ParseExpressionStatement()
    
    def ParseReturnStatement(self) -> Node:
        '''
        ReturnStatement
            | 'return' Expression ';'
            ;
        '''
        self.eat('RETURN')
        
        expression = []
        if self.lookahead.type != ';': 
            expression.append(self.ParseExpression())
            
        self.eat(';')
        
        return Node(NT.RETURN_STATEMENT, children=expression)
    
    def ParseFunctionDeclarationStatement(self) -> Node:
        '''
        FunctionDeclarationStatement
            | 'def' Identifier '(' FunctionParameters ')' BlockStatement
            ;
        '''
        self.eat('DEF')
        name = self.Identifier()
        
        self.eat('(')
        parameters = Node(NT.FUNCTION_PARAMETERS, children=[])
        if self.lookahead.type != ')':
            parameters = self.ParseFunctionParameters()
        self.eat(')')

        body = self.ParseBlockStatement()
        return Node(NT.FUNCTION_DECLARATION_STATEMENT, children=[name, parameters, body])
    
    def ParseFunctionParameters(self) -> Node:
        '''
        FunctionParameters
            | ParseFormalParameterList
            ;
        '''
        return Node(NT.FUNCTION_PARAMETERS, children=self.ParseFormalParameterList())
    
    def ParseFormalParameterList(self) -> list[Node]:
        '''
        FormalParameterList
            | Identifier
            | FormalParameterList ',' Identifier
            ;
        '''
        parameters = [self.Identifier()]
        
        while self.lookahead.type == ',':
            self.eat(',')
            parameters.append( self.Identifier() )
        
        return parameters
    
    def ParseIfStatement(self):
        '''
        If Statement
            | 'if' '(' Expression ')' Statement
            | 'if' '(' Expression ')' Statement 'else' Statement
            ;
        '''
        self.eat('IF')
        self.eat('(')
        
        children = [self.ParseExpression()]
        self.eat(')')
        
        children.append(self.ParseStatement())
        if self.lookahead and self.lookahead.type == 'ELSE':
            self.eat('ELSE')
            children.append(self.ParseStatement())

        return Node(NT.IF_STATEMENT, children=children)
    
    def ParseIterationStatement(self) -> Node:
        '''
        IterationStatement
            | WhileStatement
            | DoWhileStatement
            | ForStatement
            ;
        '''
        if self.lookahead.type == 'WHILE':
            return self.ParseWhileStatement()
        elif self.lookahead.type == 'DO':
            return self.ParseDoWhileStatement()
        elif self.lookahead.type == 'FOR':
            return self.ParseForStatement()
    
    def ParseForStatement(self) -> Node:
        '''
        ForStatement
            | 'for' '(' OptForStatementInit ';' OptExpression ';' OptExpression ')' Statement
            ;
        '''
        self.eat('FOR')
        self.eat('(')
        
        init = None
        if self.lookahead.type != ';':
            init = self.ParseForStatementInit()
        self.eat(';')
        
        test = None
        if self.lookahead.type != ';':
            test = self.ParseExpression()
        self.eat(';')
        
        update = None
        if self.lookahead.type != ')':
            update = self.ParseExpression()
        self.eat(')')
        
        body = self.ParseStatement()
        return Node(NT.FOR_LOOP_STATEMENT, children=[init, test, update, body])
    
    def ParseForStatementInit(self) -> Node:
        '''
        ForStatementInit
            | VariableStatementInit
            | ExpressionStatement
            ;
        '''
        if self.lookahead.type == 'LET':
            return self.ParseVariableStatementInit()
        return self.ParseExpression()
    
    def ParseDoWhileStatement(self) -> Node:
        '''
        DoWhileStatement
            | 'do' Statement 'while' '(' Expression ')' ';'
            ;
        '''
        self.eat('DO')
        children = [self.ParseStatement()]
        self.eat('WHILE')
        self.eat('(')
        children.append(self.ParseExpression())
        self.eat(')')
        self.eat(';')
        
        return Node(NT.DO_WHILE_LOOP_STATEMENT, children=children)
    
    def ParseWhileStatement(self) -> Node:
        '''
        WhileStatement
            | 'while' '(' Expression ')' Statement
            ;
        '''
        self.eat('WHILE')
        self.eat('(')
        
        children = [self.ParseExpression()]
        self.eat(')')
        
        children.append(self.ParseStatement())

        return Node(NT.WHILE_LOOP_STATEMENT, children=children)
    
    def CmdPrintStatement(self) -> Node:
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
        
        return Node(NT.CMD_PRINT_STATEMENT, children=[expression])


    def ParseVariableStatementInit(self) -> list[Node]:
        '''
        VariableStatementInit
            | 'let' VariableDeclarationList
            ;
        '''
        self.eat('LET')
        declarations = self.ParseVariableDeclarationList()
        return Node(NT.VARIABLE_STATEMENT, children=declarations)
    
    def ParseVariableStatement(self) -> Node:
        '''
        VariableStatement
            | VariableStatementInit ';'
            ;
        '''
        init = self.ParseVariableStatementInit()
        self.eat(';')
        return init
    
    def ParseVariableDeclarationList(self) -> list[Node]:
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
    
    def VariableDeclaration(self) -> Node:
        '''
        VariableDeclaration
            | Identifier
            | Identifier '=' Expression
            ;
        '''
        identifier = self.Identifier()

        init = None        
        out = [identifier]
        if self.lookahead.type != ';' and self.lookahead.type != ',':
            init = self.ParseVariableInitializer()
            out.append(init)

        return Node(NT.VARIABLE_DECLARATION, children=out)
    
    def ParseVariableInitializer(self) -> Node:
        '''
        VariableInitializer
            | '=' Expression
            ;
        '''
        self.eat('SIMPLE_ASSIGN')
        return self.ParseAssignmentExpression()
    
    def ParseEmptyStatement(self) -> Node:
        '''
        EmptyStatement
            | ';'
            ;
        '''
        self.eat(';')
        return Node(NT.EMPTY_STATEMENT)
    
    def ParseExpressionStatement(self) ->  Node:
        '''
        ExpressionStatement
            | Expression
            ;
        '''
        
        expression = self.ParseExpression()
        self.eat(';')
        return Node(NT.EXPRESSION_STATEMENT, children=[expression])
        
    def ParseBlockStatement(self) -> Node:
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
        
        return Node(NT.BLOCK_STATEMENT, children=body)
        
    def ParseExpression(self) -> Node:
        '''
        Expression
            | AssignmentExpression
            ;
        '''
        
        return self.ParseAssignmentExpression()
    
    def ParseAssignmentExpression(self) -> Node:
        '''
        AssignmentExpression
            | LogicalORExpression
            | LeftHandSideExpression AssignmentOperator AssignmentExpression
            ;
        '''
        left = self.ParseLogicalORExpression()
        if not self._isAssignmentOperator(self.lookahead):
            return left
        
        operator = self.ParseAssignmentOperator()
        left = self._checkValidAssignmentTarget(left)
        right = self.ParseAssignmentExpression()
        
        return Node(NT.ASSIGNMENT_EXPRESSION, operator.value, [left, right])
    
    def ParseEqualityExpression(self) -> Node:
        '''
        
        x == y
        x != y
        
        EqualityExpression
            | RelationalExpression EQUALITY_OPERATOR EqualityExpression
            | RelationalExpression
            ;
        '''
        return self._BinaryExpression('ParseRelationalExpression', 'EQUALITY_OPERATOR')
    
    def ParseRelationalExpression(self) -> Node:
        '''
        RELATIONA_OPERATOR: >, >=, <, <=
        
        x > y
        x >= y
        x < y
        x <= y
        
        RelationalExpression
            | AdditiveExpression
            | AdditiveExpression RELATIONA_OPERATOR RelationalExpression
            ;
        '''
        
        return self._BinaryExpression('ParseAdditiveExpression', 'RELATIONAL_OPERATOR')
    
    def ParseLeftHandSideExpression(self) -> Node:
        '''
        LeftHandSideExpression
            | PrimaryExpression
            ;
        '''
        return self.ParsePrimaryExpression()
    
    def Identifier(self) -> Node:
        '''
        Identifier
            | IDENTIFIER
            ;
        '''
        token = self.eat('IDENTIFIER')
        return Node(NT.IDENTIFIER, value=token.value)
        
    def _checkValidAssignmentTarget(self, target_node: Node) -> Node:
        if target_node == NT.IDENTIFIER:
            return target_node
        else:
            raise Exception('Invalid left side in assignment')
    
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
    
    def _LogicalExpression(self, builderName: str, operatorToken: str) -> Node:
        left = self.builders[builderName]()
        while self.lookahead.type == operatorToken:
            operator = self.eat(operatorToken).value
            right = self.builders[builderName]()
            left = Node(NT.BINARY_EXPRESSION, operator, [left, right])
        
        return left
    
    def ParseLogicalORExpression(self) -> Node:
        '''
        LogicalORExpression
            | LogicalANDExpression
            | LogicalORExpression LOGICAL_OR LogicalANDExpression
            ;
        '''
        return self._LogicalExpression('ParseLogicalANDExpression', 'LOGICAL_OR')
    
    def ParseLogicalANDExpression(self) -> Node:
        '''
        LogicalANDExpression
            | EqualityExpression
            | LogicalANDExpression LOGICAL_AND EqualityExpression
            ;
        '''
        return self._LogicalExpression('ParseEqualityExpression', 'LOGICAL_AND')
    
    def ParseAdditiveExpression(self) -> Node:
        '''
        AdditiveExpression
            | Literal
            | AdditiveExpression ADDITIVE_OPERATOR Literal
            ;
        '''
        return self._BinaryExpression('ParseMultiplicativeExpression', 'ADDITIVE_OPERATOR')

    def _BinaryExpression(self, builderName: str, operatorToken: str) -> Node:
        left = self.builders[builderName]()
        while self.lookahead.type == operatorToken:
            operator = self.eat(operatorToken).value
            right = self.builders[builderName]()
            left = Node(NT.BINARY_EXPRESSION, operator, [left, right])
        
        return left

    def ParseMultiplicativeExpression(self) -> Node:
        '''
        MultiplicativeExpression
            | PrimaryExpression
            | MultiplicativeExpression MULTIPLICATIVE_OPERATOR PrimaryExpression
            ;
        '''
        return self._BinaryExpression('ParseUnaryExpression', 'MULTIPLICATIVE_OPERATOR')
    
    
    def ParseUnaryExpression(self) -> Node:
        '''
        UnaryExpression
            | LeftHandSideExpression
            | ADDITIVE_OPERATOR UnaryExpression
            | LOGICAL_NOT UnaryExpression
            ;
        '''
        operator = None
        if self.lookahead.type == 'ADDITIVE_OPERATOR':
            operator = self.eat('ADDITIVE_OPERATOR').value
        elif self.lookahead.type == 'LOGICAL_NOT':
            operator = self.eat('LOGICAL_NOT').value
        
        if operator:
            return Node(NT.UNARY_EXPRESSION, operator, [self.ParseUnaryExpression()])
        
        return self.ParseLeftHandSideExpression()
    
    def ParsePrimaryExpression(self) -> Node:
        '''
        PrimaryExpression
            | Literal
            | ParenthesizedExpression
            | Identifier
            ;
        '''
        
        if self._isLiteral(self.lookahead.type):
            return self.ParseLiteral()
        
        if self.lookahead.type == '(':
            return self.ParseParenthesizedExpression()
        elif self.lookahead.type == 'IDENTIFIER':
            return self.Identifier()
        else:
            return self.ParseLeftHandSideExpression()
    
    def _isLiteral(self, token: Token) -> bool:
        return token == 'NUMBER' or token == 'STRING' or token == 'TRUE' or token == 'FALSE' or token == 'NULL'
    
    def ParseParenthesizedExpression(self) -> Node:
        '''
        ParenthesizedExpression
            | '(' Expression ')'
            ;
        '''
        self.eat('(')
        expression = self.ParseExpression()
        self.eat(')')
        
        return expression
    
    def ParseLiteral(self) -> Node:
        '''
        Literal
            | NumericLiteral
            | StringLiteral
            | BooleanLiteral
            | NullLiteral
            ;
        '''
        
        if self.lookahead.type == 'NUMBER':
            return self.NumericLiteral()
        elif self.lookahead.type == 'STRING':
            return self.StringLiteral()
        elif self.lookahead.type == 'TRUE':
            return self.BooleanLiteral(True)
        elif self.lookahead.type == 'FALSE':
            return self.BooleanLiteral(False)
        elif self.lookahead.type == 'NULL':
            return self.NullLiteral()
        else:
            raise Exception(f'Unexpected token {self.lookahead.type}')
    
    def BooleanLiteral(self, value: bool) -> Node:
        '''
        BooleanLiteral
            | 'true'
            | 'false'
            ;
        '''
        if value:
            self.eat('TRUE')
        else:
            self.eat('FALSE')
        
        return Node(NT.BOOLEAN_LITERAL, value)
    
    def NullLiteral(self) -> Node:
        '''
        NullLiteral
            | 'null'
            ;
        '''
        self.eat('NULL')
        return Node(NT.NULL_LITERAL)
    
    def StringLiteral(self) -> Node:
        '''
        StringLiteral
            | '"' [a-zA-Z0-9]* '"'
            ;
        '''
        token: Token = self.eat('STRING')
        return Node(NT.STRING_LITERAL, value=token.value[1:-1])
        
    def NumericLiteral(self) -> Node:
        '''
        NumericLiteral
            | [0-9]+
            ;
        '''
        token: Token = self.eat('NUMBER')
        return Node(NT.NUMERIC_LITERAL, value=int(token.value))
    
    def eat(self, type) -> Token:
        if self.lookahead is None:
            raise Exception('Unexpected end of input, you may be missing a semicolon \";\"')
        
        token = self.lookahead
        
        if token.type != type:
            raise Exception(f'Unexpected token {token.type}')
        
        self.lookahead = self.tokenizer.get_next_token()
        
        return token
    

class Optimizer:

    def collapse_static_binary_expressions(self, node: Node):
        if not isinstance(node, Node):
            return node
        
        for i, child in enumerate(node.children):
            node.children[i] = self.collapse_static_binary_expressions(child)

        is_static_expr = self.is_static_expression(node)
        if is_static_expr:
            return self.evaluate_static_expression(node)
            
        return node
    
    def is_static_expression(self, node: Node) -> bool:
        if node.type != NT.BINARY_EXPRESSION:
            return False
        if not isinstance(node.left(), Node) or not isinstance(node.right(), Node):
            return False

        return node.left().type == NT.NUMERIC_LITERAL and node.right().type == NT.NUMERIC_LITERAL
    
    def evaluate_static_expression(self, node: Node) -> dict:
        result = self.apply_operator(node.left().value, node.right().value, node.operator())
        return Node(NT.NUMERIC_LITERAL, value=result)
    
    def apply_operator(self, left: int, right: int, operator: str) -> int:
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left // right
        else:
            raise Exception(f'Unknown operator: {operator}')