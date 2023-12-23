from __future__ import annotations
from enum import Enum

class NT(Enum):
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
    
    INTERMEDIATE_EXPRESSION = 'IntermediateExpression'
    
    def __eq__(self, other):
        if not isinstance(other, NT):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value
    
    def all():
        return list(map(lambda c: c.value, NT))


class Node:
    
    def __init__(self, node_type: NT, value=None, children=[]) -> None:
        self.type = node_type
        self.value = value
        
        if not isinstance(children, list):
            raise Exception('Children must be a list')
        self.children: list[Node] = children if children is not None else []
        
    def __str__(self) -> str:
        return str(self.__json__())
    
    def __repr__(self) -> str:
        return str(self)
    
    def __json__(self):
        return {
            'type': self.type,
            'value': self.value,
            'children': self.children
        }
    
    def __eq__(self, other):
        if isinstance(other, NT):
            return self.type == other
        elif isinstance(other, Node):
            return self.type == other.type and self.value == other.value and self.children == other.children
        else:
            raise NotImplemented

    def __ne__(self, other):
        if isinstance(other, NT):
            return self.type != other
        else:
            raise NotImplemented

    def get_children(self) -> list[Node]:
        if not isinstance(self.children, list):
            return [self.children]
        return self.children

    def left(self) -> Node:
        if self.type == NT.BINARY_EXPRESSION and len(self.children) >= 1:
            return self.children[0]
        raise Exception('Binary expression must have at least 2 children')

    def right(self) -> Node:
        if self.type == NT.BINARY_EXPRESSION and len(self.children) >= 2:
            return self.children[1]
        raise Exception('Binary expression must have at least 2 children')

    def operator(self):
        return self.value