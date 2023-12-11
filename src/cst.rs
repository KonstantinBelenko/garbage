use crate::token::{Token, TokenType};


// IMPORTANT
// When adding a new node, make sure to add it to is_leaf() and parse_expression_or_single_value()
#[derive(Debug, PartialEq)]
pub enum ExprNode {
    IntLiteral(i32),
    StringLiteral(String),
    Variable(String),

    CommaExpr { 
        left: Box<ExprNode>,
        right: Box<ExprNode>,
    },

    BinaryExpr {
        left: Box<ExprNode>,
        operator: TokenType,
        right: Box<ExprNode>,
    },
    VariableDecl {
        var_type: TokenType,
        var_name: String,
        var_value: Box<ExprNode>,
    },
    Assignment {
        var_name: String,
        var_value: Box<ExprNode>,
    },
    PrintCommand(Vec<ExprNode>),
}

impl ExprNode {

    pub fn is_leaf(&self) -> bool {
        match self {
            ExprNode::IntLiteral(_) | ExprNode::StringLiteral(_) | ExprNode::Variable(_) => true,
            _ => false,
        }
    }

    pub fn parse_factor(tokens: &[Token]) -> Result<(ExprNode, &[Token]), String> {
        match tokens.first() {
            Some(Token { token_type: TokenType::LiteralInt, value, .. }) => {
                let int_value = value.parse::<i32>().unwrap();
                Ok((ExprNode::IntLiteral(int_value), &tokens[1..]))
            },
            Some(Token { token_type: TokenType::LiteralString, value, .. }) => {
                Ok((ExprNode::StringLiteral(value.clone()), &tokens[1..]))
            },
            Some(Token { token_type: TokenType::Name, value, .. }) => {
                Ok((ExprNode::Variable(value.clone()), &tokens[1..]))
            },
            Some(Token { token_type: TokenType::LeftParenthesis, .. }) => {
                let (expr, remaining_tokens) = ExprNode::parse_expr(&tokens[1..])?;
                match remaining_tokens.first() {
                    Some(Token { token_type: TokenType::RightParenthesis, .. }) => {
                        Ok((expr, &remaining_tokens[1..]))
                    },
                    _ => Err(format!("Expected ')' but found {:?}", remaining_tokens.first())),
                }
            },

            _ => Err(format!("Expected int literal, variable name, or expression, found {:?}", tokens.first())),
        }
    }

    pub fn parse_term(tokens: &[Token]) -> Result<(ExprNode, &[Token]), String> {
        let (mut left, mut remaining_tokens) = ExprNode::parse_factor(tokens)?;

        while let Some(token) = remaining_tokens.first() {
            match token.token_type {
                TokenType::Multiply | TokenType::Divide => {
                    let operator = token.token_type.clone();
                    let (right, next_tokens) = ExprNode::parse_factor(&remaining_tokens[1..])?;
                    remaining_tokens = next_tokens;
                    left = ExprNode::BinaryExpr {
                        left: Box::new(left),
                        operator,
                        right: Box::new(right),
                    };
                }
                _ => break,
            }
        }

        Ok((left, remaining_tokens))
    }

    pub fn parse_declaration(tokens: &[Token]) -> Result<(ExprNode, &[Token]), String> {
        if tokens.len() < 4 {
            return Err(format!("Not enough tokens for a declaration: {:?}", tokens));
        }
    
        match (tokens.get(0), tokens.get(1)) {
            (
                Some(Token { token_type: TokenType::Int, .. }) | Some(Token { token_type: TokenType::Str, .. }),
                Some(Token { token_type: TokenType::Name, value: var_name, .. })
            ) => {
                match tokens.get(2) {
                    Some(Token { token_type: TokenType::Equal, .. }) => {
                        let (expr, remaining_tokens) = ExprNode::parse_expr(&tokens[3..])?;
                        Ok((
                            ExprNode::VariableDecl {
                                var_type: tokens[0].token_type.clone(),
                                var_name: var_name.to_string(),
                                var_value: Box::new(expr),
                            },
                            remaining_tokens,
                        ))
                    }
                    _ => Err(format!("Expected '=' after variable name, found {:?}", tokens.get(2))),
                }
            }
            _ => Err(format!("Invalid token sequence for a declaration: {:?}", tokens)),
        }
    }
    

    pub fn parse_assignment(tokens: &[Token]) -> Result<(ExprNode, &[Token]), String> {
        match tokens.first() {
            Some(Token {
                token_type: TokenType::Name,
                value,
                ..
            }) => match tokens.get(1) {
                Some(Token {
                    token_type: TokenType::Equal,
                    value: _,
                    ..
                }) => {
                    let (expr, remaining_tokens) = ExprNode::parse_expr(&tokens[2..]).unwrap();
                    return Ok((
                        ExprNode::Assignment {
                            var_name: value.to_string(),
                            var_value: Box::new(expr),
                        },
                        remaining_tokens,
                    ));
                }
                _ => panic!("Expected = but found {:?}", tokens.get(1)),
            },
            _ => panic!("Expected var name but found {:?}", tokens.first()),
        }
    }

    pub fn parse_expr(tokens: &[Token]) -> Result<(ExprNode, &[Token]), String> {
        let (mut left, mut remaining_tokens) = ExprNode::parse_term(tokens)?;

        while let Some(token) = remaining_tokens.first() {
            match token.token_type {
                TokenType::Plus | TokenType::Minus => {
                    let operator = token.token_type.clone();
                    let (right, next_tokens) = ExprNode::parse_term(&remaining_tokens[1..])?;
                    remaining_tokens = next_tokens;
                    left = ExprNode::BinaryExpr {
                        left: Box::new(left),
                        operator,
                        right: Box::new(right),
                    };
                }
                _ => break,
            }
        }

        Ok((left, remaining_tokens))
    }

    pub fn parse_print_command(tokens: &[Token]) -> Result<(ExprNode, &[Token]), String> {
        let mut remaining_tokens = &tokens[1..];
        let mut print_args = Vec::new();
    
        while remaining_tokens.len() > 0 
            && remaining_tokens[0].token_type != TokenType::EOL 
            && remaining_tokens[0].token_type != TokenType::EOF {

            if remaining_tokens[0].token_type == TokenType::Comma {
                remaining_tokens = &remaining_tokens[1..];
            }

            let (expr, next_tokens) = ExprNode::parse_expression_or_single_value(remaining_tokens)?;
            print_args.push(expr);
            remaining_tokens = next_tokens;
        }
    
        if remaining_tokens.len() > 0 && (remaining_tokens[0].token_type == TokenType::EOL || remaining_tokens[0].token_type == TokenType::EOF) {
            remaining_tokens = &remaining_tokens[1..];
        }
    
        Ok((ExprNode::PrintCommand(print_args), remaining_tokens))
    }
    
    fn parse_expression_or_single_value(tokens: &[Token]) -> Result<(ExprNode, &[Token]), String> {
        match tokens.first() {
            Some(Token { token_type: TokenType::Name, .. })
            | Some(Token { token_type: TokenType::LiteralInt, .. })
            | Some(Token { token_type: TokenType::LiteralString, .. })
            | Some(Token { token_type: TokenType::LeftParenthesis, .. }) => {
                ExprNode::parse_expr(tokens)
            }
            _ => Err(format!("Expected expression or value, found {:?}", tokens.first())),
        }
    }

    pub fn parse(tokens: &[Token]) -> Result<(ExprNode, &[Token]), String> {
        match tokens.first() {
            Some(Token { token_type: TokenType::Int,  .. }) | Some(Token { token_type: TokenType::Str, .. }) => {
                let val = ExprNode::parse_declaration(tokens);
                return val;
            }
            Some(Token { token_type: TokenType::Name, .. }) => {
                return ExprNode::parse_assignment(tokens);
            }
            Some(Token { token_type: TokenType::CmdPrint, .. }) => {
                return ExprNode::parse_print_command(tokens);
            }
            _ => Err(format!("Invalid token: {:?}", tokens.first())),
        }
    }

    pub fn parse_all(tokens: &[Token]) -> Result<Vec<ExprNode>, String> {
        let mut expressions = Vec::new();
        let mut remaining_tokens = tokens;

        while remaining_tokens.len() > 0 && remaining_tokens[0].token_type != TokenType::EOF {
            let (expr, next_tokens) = ExprNode::parse(remaining_tokens)?;
            expressions.push(expr);
            remaining_tokens = next_tokens;

            while matches!(remaining_tokens.get(0).map(|t| &t.token_type), Some(TokenType::EOL)) {
                remaining_tokens = &remaining_tokens[1..];
            }
        }

        return Ok(expressions);
    }
}

pub fn pretty_print_expr(expr: &ExprNode, indent: usize) {
    match expr {
        ExprNode::BinaryExpr {
            left,
            operator,
            right,
        } => {
            println!("{}BinaryExpr", " ".repeat(indent));
            println!("{}Operator: {:?}", " ".repeat(indent + 2), operator);
            println!("{}Left:", " ".repeat(indent + 2));
            pretty_print_expr(left, indent + 4);
            println!("{}Right:", " ".repeat(indent + 2));
            pretty_print_expr(right, indent + 4);
        }
        ExprNode::VariableDecl {
            var_type,
            var_name,
            var_value,
        } => {
            println!("{}VariableDecl", " ".repeat(indent));
            println!("{}Type: {:?}", " ".repeat(indent + 2), var_type);
            println!("{}Name: {}", " ".repeat(indent + 2), var_name);
            println!("{}Value:", " ".repeat(indent + 2));
            pretty_print_expr(var_value, indent + 4);
        }
        ExprNode::Assignment {
            var_name,
            var_value,
        } => {
            println!("{}Assignment", " ".repeat(indent));
            println!("{}Name: {}", " ".repeat(indent + 2), var_name);
            println!("{}Value:", " ".repeat(indent + 2));
            pretty_print_expr(var_value, indent + 4);
        }
        ExprNode::PrintCommand(exprs) => {
            println!("{}PrintCommand", " ".repeat(indent));
            for expr in exprs {
                pretty_print_expr(expr, indent + 2);
            }
        }
        ExprNode::IntLiteral(value) => {
            println!("{}IntLiteral: {}", " ".repeat(indent), value);
        }
        ExprNode::StringLiteral(value) => {
            println!("{}StringLiteral: {}", " ".repeat(indent), value);
        }
        ExprNode::Variable(name) => {
            println!("{}Variable: {}", " ".repeat(indent), name);
        }
        ExprNode::CommaExpr { left, right } => {
            println!("{}CommaExpr", " ".repeat(indent));
            println!("{}Left:", " ".repeat(indent + 2));
            pretty_print_expr(left, indent + 4);
            println!("{}Right:", " ".repeat(indent + 2));
            pretty_print_expr(right, indent + 4);
        }
    }
}
