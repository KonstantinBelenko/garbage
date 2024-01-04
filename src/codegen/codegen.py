from src.parser import NT, Node
from .static_functions import static_funcions

class Codegen:
    def __init__(self, ast: Node) -> None: ...
    def compile(self) -> list[str]: ...

class Codegen_V3(Codegen):
    
    def __init__(self, ast: Node) -> None:
        self.ast = ast
        self.asm_code = ['.global _main']
        self.include = set(['terminate_program'])
        self.literal_counter = 0
    
    def compile(self) -> list[str]:
        print('Compiling')
        self._preprocess_data_section()
        self._compile_node(self.ast)
        self._include()
        return self.asm_code
    
    def _preprocess_data_section(self):
        print(':data section')
        self.asm_code.append('.data')
        self._preprocess_data_node(self.ast)
        print('\n')
        
    def _preprocess_data_node(self, node: Node, level=0):
        print('  '*level, 'node:', node.type)
        
        for child in node.get_children():
            self._preprocess_data_node(child, level+1)
        
        if node.type == NT.STRING_LITERAL:
            self._process_string_literal(node, level+1)
    
    def _process_string_literal(self, node: Node, level=0):
        print('  '*level, 'string literal:', node.value)
        self.asm_code.append('.align 3')
        self.asm_code.append('.LC%s: .string "%s"' % (str(self.literal_counter), node.value.replace('\n', '\\n')))
        node.value = '.LC%s' % str(self.literal_counter)
        self.literal_counter += 1
    
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
        elif node.type == NT.CMD_PRINT_STATEMENT:
            self._compile_cmd_print_statement(node, level+1)
        elif node.type == NT.STRING_LITERAL:
            self._compile_string_literal(node, level+1)
        else:
            raise NotImplementedError('Node type %s not implemented' % node.type)
    
    def _compile_program(self, node: Node, level=0):
        print('  '*level, 'program')
        self.asm_code.append('.text')
        self.asm_code.append('_main:')
        self.asm_code.append('sub sp, sp, #16')
        for child in node.get_children():
            self._compile_node(child, level+1)
        self.asm_code.append('mov w0, #0')
        self.asm_code.append('add sp, sp, #16')
        self.asm_code.append('b terminate_program')
    
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
    
    def _compile_cmd_print_statement(self, node: Node, level=0):
        print('  '*level, 'cmd print statement')
        self.include.add('print_string')
        for child in node.get_children():
            self._compile_node(child, level+1)
        self.asm_code.append('ldr w0, [sp, 4]')
        self.asm_code.append('bl print_string')
    
    def _compile_string_literal(self, node: Node, level=0):
        print('  '*level, 'string literal:', node.value)
        self.asm_code.append('adrp x0, %s@PAGE' % node.value)
        self.asm_code.append('add x0, x0, %s@PAGEOFF' % node.value)
    
    def _include(self):
        asm = []
        for func in self.include:
            if func in static_funcions:
                asm.extend(static_funcions[func]())
            else:
                raise NotImplementedError('Function %s not implemented' % func)
        
        self.asm_code.extend(asm)