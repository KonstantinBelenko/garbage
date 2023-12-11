use regex::Regex;
use lazy_static::lazy_static;

lazy_static! {
    static ref VAR_NAME_REGEX: Regex = Regex::new(r"^[a-zA-Z_][a-zA-Z0-9_]*$").unwrap();
    static ref INT_REGEX: Regex = Regex::new(r"^[0-9]+$").unwrap();
}

#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {

    // Types
    Int, Str,

    // Names
    Name,

    // Operators
    Equal, Plus, Minus, Multiply, Divide,

    // Literals
    LiteralInt, LiteralString,

    // Special commands
    CmdPrint,

    // Special characters
    DoubleQuote, Comma,
    LeftParenthesis, RightParenthesis,
    EOL, EOF,
}

impl TokenType {
    pub fn from_str(s: &str, line: u32) -> Option<TokenType> {
        match s {
            "int" => Some(TokenType::Int),
            "str" => Some(TokenType::Str),

            "=" => Some(TokenType::Equal),
            "+" => Some(TokenType::Plus),
            "-" => Some(TokenType::Minus),
            "*" => Some(TokenType::Multiply),
            "/" => Some(TokenType::Divide),

            "(" => Some(TokenType::LeftParenthesis),
            ")" => Some(TokenType::RightParenthesis),
            "\"" => Some(TokenType::DoubleQuote),
            "," => Some(TokenType::Comma),

            "_print" => Some(TokenType::CmdPrint),

            "\n" => Some(TokenType::EOL),
            "" => Some(TokenType::EOF),

            // use regex to match the var name
            _ if VAR_NAME_REGEX.is_match(s) => Some(TokenType::Name),
            _ if INT_REGEX.is_match(s) => Some(TokenType::LiteralInt),
            _ => panic!("Unknown token type: {} on line {}", s, line),
        }
    }
}


#[derive(Debug)]
pub struct Token {
    pub token_type: TokenType,
    pub value: String,
    pub line: u32,
}
impl Token {
    pub fn new(token_type: TokenType, value: String, line: u32) -> Token {
        Token {
            token_type,
            value,
            line,
        }
    }

    pub fn from_str(s: &str, line: u32) -> Option<Token> {
        match TokenType::from_str(s, line) {
            Some(token_type) => Some(Token::new(token_type, s.to_string(), line)),
            None => panic!("Unknown token type: {} on line {}", s, line),
        }
    }
}