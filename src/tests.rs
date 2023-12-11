use super::*;

use crate::cst::ExprNode;
use crate::lexer::tokenize;
use crate::token::TokenType;

fn bin_expr(left: ExprNode, operator: TokenType, right: ExprNode) -> ExprNode {
    ExprNode::BinaryExpr {
        left: Box::new(left),
        operator,
        right: Box::new(right),
    }
}

fn var_decl(name: &str, var_type: TokenType, value: ExprNode) -> ExprNode {
    ExprNode::VariableDecl {
        var_name: name.to_string(),
        var_type,
        var_value: Box::new(value),
    }
}

fn int_lit(value: i32) -> ExprNode {
    ExprNode::IntLiteral(value)
}

fn var(name: &str) -> ExprNode {
    ExprNode::Variable(name.to_string())
}

#[test]
fn test_order_of_operations() {
    let test_cases = vec![
        (
            "int a = 1 + 2 * 3",
            var_decl("a", TokenType::Int, bin_expr(int_lit(1), TokenType::Plus, bin_expr(int_lit(2), TokenType::Multiply, int_lit(3))))
        ),
        (
            "int d = 4 + 12 / 3 * 2",
            var_decl("d", TokenType::Int, bin_expr(int_lit(4), TokenType::Plus, bin_expr( bin_expr(int_lit(12), TokenType::Divide, int_lit(3)), TokenType::Multiply, int_lit(2))))
        )
    ];

    for (expression, expected_ast) in test_cases {
        println!("Testing expression: {}", expression);
        let tokens = tokenize(expression);
        let ast = ExprNode::parse_all(&tokens).unwrap();
        assert_eq!(ast, vec![expected_ast]);
    }
}
