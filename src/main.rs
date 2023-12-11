mod lexer;
mod token;
mod cst;
mod semantic;
mod codegen;

#[cfg(test)]
mod tests;

use std::env;
use cst::pretty_print_expr;

use crate::codegen::generate_code;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Please provide a file path as an argument");
        return;
    }

    let file_path = &args[1];
    let tokens = lexer::tokenize_file(file_path)
        .expect("Failed to tokenize file");
    
    tokens.iter().all(|t| { println!("{:?}", t); true });
    println!("");

    let syntax_tree = cst::ExprNode::parse_all(&tokens)
        .expect("Failed to parse tokens");

    syntax_tree.iter().for_each(|n| pretty_print_expr(n, 0));
}

