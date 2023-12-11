use crate::{token::TokenType, cst::ExprNode}; // Assuming TokenType is defined elsewhere

pub fn generate_code_for_node(node: ExprNode) -> String {
    match node {
        ExprNode::StringLiteral(s) => {
            format!(".data\n.align 3\nstring: .ascii \"{}\"\n", s)
        },
        ExprNode::IntLiteral(i) => {
            format!(".data\nnumber: .word {}\n", i)
        },
        ExprNode::PrintCommand(exprs) => {
            let mut print_code = String::new();
            for expr in exprs {
                print_code.push_str(&generate_code_for_node(expr));
                print_code.push_str("    MOV x0, #1\n    LDR x1, [string]\n    MOV x16, #4\n    SVC 0\n");
            }
            print_code
        },
        // ... Implement other cases ...
        _ => String::from("// Unhandled node type\n")
    }
}

pub fn generate_code(ast: Vec<ExprNode>) -> String {
    let mut code = String::from(".text\n.global _start\n_start:\n");
    for node in ast {
        code.push_str(&generate_code_for_node(node));
    }
    code.push_str("    MOV x0, 0\n    MOV x16, #1\n    SVC 0\n"); // Example: Exit code
    code
}