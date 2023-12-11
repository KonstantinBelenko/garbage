use crate::token::{Token, TokenType};

pub fn tokenize(contents: &str) -> Vec<Token> {
    let mut tokens: Vec<Token> = Vec::new();
    let mut line_number = 1;
    let mut current_token = String::new();
    let mut in_string_literal = false;

    for c in contents.chars() {
        if in_string_literal {
            if c == '"' {
                tokens.push(Token::new(TokenType::LiteralString, current_token.clone(), line_number));
                current_token.clear();
                in_string_literal = false;
            } else {
                current_token.push(c);
            }
        } else {
            match c {
                ' ' | '\t' | '\r'  => {
                    if !current_token.is_empty() {
                        if let Some(token) = Token::from_str(&current_token, line_number) {
                            tokens.push(token);
                        }
                        current_token.clear();
                    }
                },
                '(' | ')' | '+' | '-' | '*' | '/' | '=' | '"' | ',' => {
                    if !current_token.is_empty() {
                        if let Some(token) = Token::from_str(&current_token, line_number) {
                            tokens.push(token);
                        }
                        current_token.clear();
                    }
                    if c == '"' {
                        in_string_literal = true;
                    } else {
                        tokens.push(Token::new(TokenType::from_str(&c.to_string(), line_number).unwrap(), c.to_string(), line_number));
                    }
                },
                '\n' => {
                    line_number += 1;
                    if !current_token.is_empty() {
                        if let Some(token) = Token::from_str(&current_token, line_number) {
                            tokens.push(token);
                        }
                        current_token.clear();
                    }
                    tokens.push(Token::new(TokenType::EOL, "\n".to_string(), line_number));
                },
                _ => {
                    current_token.push(c);
                }
            }
        }
    }

    // Handle the last token if any
    if !current_token.is_empty() {
        if let Some(token) = Token::from_str(&current_token, line_number) {
            tokens.push(token);
        }
    }
    tokens.push(Token::new(TokenType::EOF, "".to_string(), line_number));

    return tokens;
}

pub fn tokenize_file(file_path: &str) -> Result<Vec<Token>, std::io::Error> {
    let contents = std::fs::read_to_string(file_path)?;
    let tokens = tokenize(&contents);

    return Ok(tokens);
}