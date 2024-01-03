from src.parser import NT, Node
from .static_functions import static_funcions


class CodeGen_v2:
    
    def __init__(self) -> None:
        self.used_commands = set()
        self.global_label_counter = 0

    def generate(self, ast: dict) -> list[str]:
        asm = ['.global _main']
        self.used_commands = set()
        self.used_commands.add('terminate_program')
        self.global_label_counter = 0
        
        data_run = self.generate_data(ast)
        text_run = self.generate_text(ast)
        
        for cmd in self.used_commands:
            asm.extend(static_funcions[cmd]())
            
        asm.extend(data_run)
        asm.extend(text_run)
        
        return asm

    def generate_data(self, node: Node) -> list[str]:
        data_asm = []
        data_asm.append('.data')
        
        print(' --- data start --- ')
        print('Descent into tree')
        for i, child in enumerate(node.children):
            print('Root Branch:', child.type)
            asm, new_child = self.generate_data_descent(child)
            data_asm.extend(asm)
        
        print('Root return from descent. asm:', data_asm)
        print(' --- data end --- \n\n')
        
        return data_asm
    
    def generate_data_descent(self, node: Node) -> tuple[list[str], Node]:
        asm = []
        
        for i, child in enumerate(node.children):
            print('branch:', child.type)
            code, new_child = self.generate_data_node(child)
            asm.extend(code)

        if node:
            new_asm, node = self.generate_data_node(node)
            asm.extend(new_asm)
        
        print('Return from descent. asm:', asm)

        return asm, node

    def generate_data_node(self, node: Node) -> tuple[list[str], Node]:
        asm = []
        print('generating data node:', node.type)
        if node.type == NT.NUMERIC_LITERAL:
            label_name = self.gen_label_name()
            node.label_name = label_name
            asm.extend([
                '.align 3',
                '%s: .word %s' % (label_name, node.value,)
            ])
            return asm, None

        elif node.type == NT.STRING_LITERAL:
            label_name = self.gen_label_name()
            node.label_name = label_name
            asm.extend([
                '.align 3',
                '%s: .asciz "%s"' % (label_name, node.value,)
            ])
            return asm, None
        
        elif node.type == NT.CMD_PRINT_STATEMENT:
            self.used_commands.add('print_string')
            if node.children[0].type == NT.NUMERIC_LITERAL:
                self.used_commands.add('itoa')
            return asm, node
        else:
            return asm, node
    
    def generate_text(self, node: Node) -> list[str]:
        test_asm = []
        test_asm.append('.text')
        test_asm.append('_main:')
        
        print(' --- text start --- ')
        print('Descent into tree')
        for child in node.children:
            print('Root Branch:', child.type)
            asm, node = self.generate_text_descent(child)
            test_asm.extend(asm)
        
        test_asm.append('b terminate_program')
        print(' --- text end --- \n\n')
        
        return test_asm
    
    def generate_text_descent(self, node: Node) -> tuple[list[str], Node]:
        asm = []
        
        for i, child in enumerate(node.children):
            print('branch:', child.type)
            code, new_child_node = self.generate_text_descent(child)
            asm.extend(code)
        
        if node is not None:
            new_asm, node = self.generate_text_node(node)
            asm.extend(new_asm)
        
        print('Return from descent. asm:', asm)
        return asm, node
    
    def generate_text_node(self, node: Node) -> tuple[list[str], Node]:
        asm = []
        if node.type == NT.NUMERIC_LITERAL:
            asm.extend([
                'adrp x0, %s@PAGE' % node.label_name,
                'ldr x0, [x0, %s@PAGEOFF]' % node.label_name,
            ])
            return asm, None
        elif node.type == NT.STRING_LITERAL:
            asm.extend([
                'adrp x0, %s@PAGE' % node.label_name,
                'add x0, x0, %s@PAGEOFF' % node.label_name,
            ])
            return asm, None
        elif node.type == NT.CMD_PRINT_STATEMENT:
            if node.children[0].type == NT.NUMERIC_LITERAL:
                asm.extend([
                    'bl itoa',
                    'mov x0, #1',
                    'mov x16, #4',
                    'svc 0',
                    'add sp, sp, x2'
                ])
            else:
                asm.extend([
                    'mov x1, x0',
                    'bl print_string',
                ])
            return asm, None
        else:
            return asm, node
            
    def gen_label_name(self) -> str:
        name = 'literal_%s' % self.global_label_counter
        self.global_label_counter += 1
        return name


class Codegen_V3:
    
    def __init__(self, ast: Node) -> None:
        self.ast = ast
        self.asm_code = []
    
    def compile(self) -> list[str]:
        print('Compiling')
        self._compile_node(self.ast)
        return self.asm_code
    
    def _compile_node(self, node: Node, level=0):
        print('  '*level, 'node:', node.type)
        if node.type == NT.PROGRAM:
            self._compile_program(node, level+1)
        elif node.type == NT.VARIABLE_STATEMENT:
            self._compile_variable_statement(node, level+1)
        elif node.type == NT.VARIABLE_DECLARATION:
            self._compile_variable_declaration(node, level+1)
        elif node.type == NT.BINARY_EXPRESSION:
            self._compile_binary_expression(node, level+1)
        else:
            raise NotImplementedError('Node type %s not implemented' % node.type)
    
    def _compile_program(self, node: Node, level=0):
        print('  '*level, 'program')
        self.asm_code.append('.global: main')
        self.asm_code.append('main:')
        self.asm_code.append('sub sp, sp, #16')
        for child in node.get_children():
            self._compile_node(child, level+1)
        self.asm_code.append('mov w0, #0')
        self.asm_code.append('add sp, sp, #16')
        self.asm_code.append('ret')
    
    def _compile_variable_statement(self, node: Node, level=0):
        print('  '*level, 'variable statement')
        for child in node.get_children():
            self._compile_node(child, level+1)
    
    def _compile_variable_declaration(self, node: Node, level=0):
        print('  '*level, 'variable declaration')
        identifier, value = node.get_children()
        if value.type == NT.NUMERIC_LITERAL:
            self.asm_code.append('mov w0, #%s' % value.value)
            self.asm_code.append('str w0, [sp, 12]')
        elif value.type == NT.IDENTIFIER:
            self.asm_code.append('ldr w0, [sp, 12]')
            self.asm_code.append('str w0, [sp, 8]')
        elif value.type == NT.BINARY_EXPRESSION:
            self._compile_binary_expression(value, level+1)
    
    def _compile_binary_expression(self, node: Node, level=0):
        print('  '*level, 'binary expression')
        left, right, operator = node.left(), node.right(), node.operator()
        if operator == '+':
            self.asm_code.append('ldr w1, [sp, 12]')
            self.asm_code.append('ldr w0, [sp, 8]')
            self.asm_code.append('add w0, w1, w0')
            self.asm_code.append('str w0, [sp, 4]')