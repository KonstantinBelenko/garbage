from src.parser import NT, Node

class StaticFunctions:
    
    @staticmethod
    def terminate_program() -> list[str]:
        return [
            'terminate_program:',
            'mov x0, #0',
            'mov x16, #1',
            'svc 0',
        ]
        
    @staticmethod
    def print_string() -> list[str]:
        return [
            'print_string:',
            'ldrb w2, [x1]',
            'cmp w2, #0',
            'beq _print_string_end',
            'mov x3, x1',
            'mov x0, 1',
            'mov x2, 1',
            'mov x16, 4',
            'svc 0',
            'mov x1, x3',
            'add x1, x1, #1',
            'b print_string',
            '_print_string_end:',
            'ret',
        ]

static_funcions = {
    'terminate_program': StaticFunctions.terminate_program,
}

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
        
        print('Descent into tree')
        for child in node.children:
            print('Root Branch:', child.type)
            asm, node = self.generate_data_descent(child)
            data_asm.extend(asm)
        
        print('Root return from descent. asm:', data_asm, '\n\n')
        return data_asm
    
    def generate_data_descent(self, node: Node) -> tuple[list[str], Node]:
        asm = []
        
        for i, child in enumerate(node.children):
            print('branch:', child.type)
            code, node = self.generate_data_node(child)
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
    
    def generate_text(self, node: Node) -> list[str]:
        test_asm = []
        test_asm.append('.text')
        test_asm.append('_main:')
        
        # ...
        
        test_asm.append('b terminate_program')
        return test_asm
        
    
    def generate_text_node(self, node: Node) -> list[str]:
        asm = []
        if node.type == NT.NUMERIC_LITERAL:
            asm.extend([
                'adrp x0, %s@PAGE' % node.asm_literal_label,
                'ldr x0, [x0, %s@PAGEOFF]' % node.asm_literal_label,
            ])
        elif node.type == NT.STRING_LITERAL:
            asm.extend([
                'adrp x0, %s@PAGE' % node.asm_literal_label,
                'add x0, x0, %s@PAGEOFF' % node.asm_literal_label,
            ])
        return asm
    
    def gen_label_name(self) -> str:
        name = 'literal_%s' % self.global_label_counter
        self.global_label_counter += 1
        return name
class CodeGenerator:
    
    def __init__(self) -> None:
        self.assembly = []
        self.literals_map = {}
        self.literal_counter = 0
        self.required_commands = set()
        self.var_name_to_node = {}
    
    def generate(self, ast: dict) -> list[str]:
        
        self.assembly.extend([
            '.global _main',
        ])
        
        section_data = self.generate_data(ast)
        section_text = self.generate_text(ast)
        
        for cmd in self.required_commands:
            self.assembly.extend(self._generate_command(cmd))
        
        self.assembly.extend(section_data)
        self.assembly.extend(section_text)
        
        return self.assembly
    
    def generate_data(self, ast: dict) -> list[str]:
        data_section = ['.data']

        def handle_node(node: dict):
            node_type = node['type']
            if node_type == NT.VARIABLE_DECLARATION:
                self.var_name_to_node[node['id']['name']] = node
                
                var_name = node['id']['name']
                init = node['init']
                if not init:
                    data_section.extend([
                        '.align 3',
                        '%s: .word 0' % (var_name,)
                    ])
                else:
                    handle_init(init, var_name)
            
            elif node_type == NT.NUMERIC_LITERAL:
                if 'asm_literal_label' not in node:
                    literal_label = f'literal_{self.literal_counter}'
                    node['asm_literal_label'] = literal_label
                    self.literals_map[node['value']] = literal_label
                    self.literal_counter += 1
                    data_section.extend([
                        '.align 3',
                        '%s: .word %s' % (literal_label, node['value'],)
                    ])
            
            elif node_type == NT.STRING_LITERAL:
                literal_label = f'literal_{self.literal_counter}'
                node['asm_literal_label'] = literal_label
                self.literals_map[node['value']] = literal_label
                data_section.extend([
                    '.align 3',
                    '%s: .asciz "%s"' % (literal_label, node['value'],)
                ])
                self.literal_counter += 1
        
        def handle_init(init: dict, var_name: str):
            if init['type'] == NT.NUMERIC_LITERAL:
                print('init', init)
                data_section.extend([
                    '.align 3',
                    '%s: .word %s' % (var_name, init['value'],)
                ])
            elif init['type'] == NT.STRING_LITERAL:
                data_section.extend([
                    '.align 3',
                    '%s: .asciz "%s"' % (var_name, init['value'],)
                ])

        self._traverse_ast(ast, handle_node)
        return data_section
    
    def generate_text(self, ast: dict) -> list[str]:
        text_section = ['.text', '_main:']
        
        def handle_node(node: dict):
            node_type = node.get('type')
            if node_type == NT.CMD_PRINT_STATEMENT:
                self.required_commands.add('print_string')
                text_section.extend(self._generate_cmd_print(node))
            elif node_type == NT.VARIABLE_DECLARATION:
                text_section.extend(self._generate_variable_declaration(node))
        
        self._traverse_ast(ast, handle_node)
        text_section.extend(['mov x0, #0', 'mov x16, #1', 'svc 0' ])
        return text_section

    def _traverse_ast(self, node: dict, handler):
        handler(node)
        for key, value in node.items():
            if isinstance(value, dict):
                self._traverse_ast(value, handler)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._traverse_ast(item, handler)

    def _generate_variable_declaration(self, node: dict) -> list[str]:
        # Cases of dynamic variable declaration:
        # | A = B
        # | A = EXPRESSION
        raise NotImplementedError('Variable declaration not implemented')

    def _generate_cmd_print(self, node: dict) -> list[str]:
        print_instructions = []
        value_node = node['body']
        value_node_type = value_node.get('type')

        if value_node_type == NT.STRING_LITERAL:
            literal_label = self.literals_map.get(value_node.get('value'))
            if literal_label:
                print_instructions.extend(self._generate_print_string_asm(literal_label))
            else:
                raise ValueError('String literal not found in literals map')
        
        elif value_node_type == NT.NUMERIC_LITERAL:
            self.required_commands.add('itoa')
            literal_label = self.literals_map.get(value_node.get('value'))
            if literal_label:
                print_instructions.extend(self._generate_print_int_asm(literal_label))
            else:
                raise ValueError('Numeric literal not found in literals map')
        
        elif value_node_type == NT.IDENTIFIER:
            var_name = value_node.get('name')
            var_node = self.var_name_to_node.get(var_name)
            var_type = var_node.get('init').get('type')
            if var_type == NT.STRING_LITERAL:
                literal_label = self.literals_map.get(var_node.get('init').get('value'))
                if literal_label:
                    print_instructions.extend(self._generate_print_string_asm(literal_label))
                else:
                    raise ValueError('String literal not found in literals map')
            elif var_type == NT.NUMERIC_LITERAL:
                self.required_commands.add('itoa')
                literal_label = self.literals_map.get(var_node.get('init').get('value'))
                if literal_label:
                    print_instructions.extend(self._generate_print_int_asm(literal_label))
                else:
                    raise ValueError('Numeric literal not found in literals map')
        else:
            raise ValueError('Unsupported print statement')

        return print_instructions

    def _generate_print_string_asm(self, label: str) -> list[str]:
        return [
            'adrp x1, %s@PAGE' % label,                 # Load the page address of the string
            'add x1, x1, %s@PAGEOFF' % label,           # Add the offset to the page address
            'bl print_string'                           # Branch to print_string function
        ]
    
    def _generate_print_int_asm(self, label: str) -> list[str]:
        return [
            'adrp x0, %s@PAGE' % label,                     # Load the page address of the string
            'ldr x0, [x0, %s@PAGEOFF]' % label,             # Add the offset to the page address
            'bl itoa',                                      # Branch to int_to_string function
            'bl print_string',                              # Branch to print_string function
            'add sp, sp, x10'                               # Clean up the stack
        ]

    def _generate_command(self, cmd):
        if cmd == 'print_string':
            return self._generate_print_string_command()
        elif cmd == "itoa":
            return self._generate_int_to_string_command()
        return []
    
    def _generate_print_string_command(self):
        return [
            'print_string:',
            'ldrb w2, [x1]',
            'cmp w2, #0',
            'beq _print_string_end',
            'mov x3, x1',
            'mov x0, 1',
            'mov x2, 1',
            'mov x16, 4',
            'svc 0',
            'mov x1, x3',
            'add x1, x1, #1',
            'b print_string',
            '_print_string_end:',
            'ret',
        ]

    def _generate_int_to_string_command(self) -> list[str]:
        return [
            'itoa:',
            'mov x2, x0',
            'mov x3, #0',
            'mov x4, #10',
            'mov x5, #0',
            '.itoa_count_loop:',
            'cmp x2, #0',
            'beq .itoa_count_end',
            'udiv x2, x2, x4',
            'add x3, x3, #1',
            'b .itoa_count_loop',
            '.itoa_count_end:',
            'mov x10, x3',
            'add x10, x10, #1',
            'sub sp, sp, x10',
            'mov x1, sp',
            'mov x2, x0',
            'mov x3, #0',
            'mov x4, #10',
            'mov x5, #0',
            'mov x6, #0',
            '.itoa_loop:',
            'udiv x6, x2, x4',
            'msub x3, x6, x4, x2',
            'add x3, x3, #48',
            'strb w3, [x1, x5]',
            'mov x2, x6',
            'add x5, x5, #1',
            'cmp x2, #0',
            'bne .itoa_loop',
            'mov x3, #10',
            'strb w3, [x1, x5]',
            'mov x7, #0',
            'sub x8, x5, #1',
            '.reverse_loop:',
            'cmp x7, x8',
            'bge .reverse_done',
            'ldrb w9, [x1, x7]',
            'ldrb w2, [x1, x8]',
            'strb w9, [x1, x8]',
            'strb w2, [x1, x7]',
            'add x7, x7, #1',
            'sub x8, x8, #1',
            'b .reverse_loop',
            '.reverse_done:',
            'mov x2, x10',
            'ret',
        ]

# class CodeGenerator:
#     '''
#     CodeGenerator is a class that generates assembly code from an AST.
#     '''
#     def __init__(self) -> None:
#         self.assembly = []
#         self.literals_map = {}
#         self.literal_count = 0

#     def generate(self, ast: dict) -> str:
#         self.assembly = []
#         self.literal_count = 0
        
#         self._generate_entry()
        
#         self.assembly.append('.data')
#         self._generate_data(ast)
        
#         self.assembly.append('\n.text\n_main:')
#         self._generate_text(ast)
        
#         self._generate_exit()
        
#         # Join the sections with appropriate line breaks, adding an extra newline between sections
#         formatted_assembly = '\n'.join(self.assembly)
#         return formatted_assembly
    
    
#     def _generate_entry(self):
#         '''
#         Appends entry instructions
#         '''
        
#         entry_instructions = [
#             ".global _main",
#             ".align 3"
#         ]
        
#         self.assembly.append(
#             "%s\n%s\n" % (
#                 entry_instructions[0], 
#                 entry_instructions[1],
#             )
#         )
    
#     def _generate_exit(self):
#         '''
#         Appends exit syscall to the text section.
#         '''

#         exit_instructions = [ 
#             'mov x0, #0',
#             'mov x16, #1',
#             'svc 0',
#         ]
        
#         self.assembly.append(
#             '    %s\n    %s\n    %s' % (
#                 exit_instructions[0], 
#                 exit_instructions[1], 
#                 exit_instructions[2]
#             )
#         )

#     def _generate_data(self, node: dict) -> None:
#         node_type = node.get('type')

#         if node_type == 'Program':
#             for child in node.get('body', []):
#                 self._generate_data(child)

#         elif node_type == 'VariableDeclaration':
#             for declaration in node.get('declarations', []):
#                 self._generate_data(declaration)
        
#         elif node_type == 'VariableDeclarator':
#             var_name = node.get('id').get('name') 
#             init = node.get('init')

#             if init and init.get('type') == 'NumericLiteral':
#                 value = init.get('value')
#                 self.assembly.append(f'    {var_name}: .word {value}')
#             elif init and init.get('type') == 'StringLiteral':
#                 value = init.get('value')
#                 self.assembly.append(f'    {var_name}: .asciz "{value}"')
#             else:
#                 self.assembly.append(f'    {var_name}: .word 0')

#         elif node_type == 'ExpressionStatement':
#             self._generate_data(node.get('body'))

#         elif node_type == 'BinaryExpression':
#             self._generate_data(node.get('left'))
#             self._generate_data(node.get('right'))

#         elif node_type == 'NumericLiteral':
#             if node.get('value') in self.literals_map:
#                 node['asm_literal_label'] = self.literals_map[node.get('value')]
#             else:
#                 node['asm_literal_label'] = self.literal_count
#                 self.literals_map[node.get('value')] = self.literal_count
#                 self.literal_count += 1
                
#                 literal_label = f'literal_{node.get("asm_literal_label")}'
#                 value = node.get('value')
                
#                 self.assembly.append(f'    {literal_label}: .word {value}')

#         elif node_type == 'StringLiteral':
#             if node.get('value') in self.literals_map:
#                 node['asm_literal_label'] = self.literals_map[node.get('value')]
#             else:
#                 node['asm_literal_label'] = self.literal_count
#                 self.literals_map[node.get('value')] = self.literal_count
#                 self.literal_count += 1
                
#                 literal_label = f'literal_{node.get("asm_literal_label")}'
#                 value = node.get('value')
                
#                 self.assembly.append(f'    {literal_label}: .asciz "{value}"')

#         elif node_type == 'CmdPrintStatement':
#             self._generate_data(node.get('body'))
    
#     def _generate_text(self, node: dict) -> None:
#         node_type = node.get('type')

#         if node_type == 'Program':
#             for child in node.get('body', []):
#                 self._generate_text(child)
        
#         elif node_type == 'ExpressionStatement':
#             self._generate_text(node.get('body'))
        
#         elif node_type == 'VariableDeclaration':
#             for declaration in node.get('declarations', []):
#                 self._generate_text(declaration)
                
#         elif node_type == 'VariableDeclarator':
#             var_name = node.get('id').get('name')
#             init = node.get('init')

#             if init:
#                 init_type = init.get('type')
#                 if init_type == 'BinaryExpression':
#                     intermediate_node = self._generate_binary_expression(init)
#                     self._generate_intermediate_assignment(intermediate_node, var_name)
        
#         # Print
#         elif node_type == 'CmdPrintStatement':
#             self._generate_print(node)
            
#     def _generate_print(self, node: dict) -> None:
#         '''
#         Generates assembly to print a value.
#         '''
        
#         value = node.get('body')
#         if value.get('type') == 'StringLiteral':
#             self._generate_print_string(value)
#         if value.get('type') == 'NumericLiteral' or value.get('type') == 'Identifier':
#             self._generate_print_numeric(value)
#         elif value.get('type') == 'BinaryExpression':
#             result = self._generate_binary_expression(value)
#             self._generate_print_numeric(result)
    
#     def _generate_print_numeric(self, node: dict) -> None:
#         '''
#         Generates assembly to print a numeric value by converting it to a string.
#         '''

#         # Load the numeric value or variable into a register
#         value_register = self._load_operand(node, 'x0', 'w0')

#         # Convert the number in the register to a string
#         self.assembly.append(f'    mov x0, {value_register}')  # Move the value to x0 for conversion
#         self.assembly.append(f'    bl convert_number_to_string')

#         # Print the string
#         self.assembly.append(f'    mov x0, #1')  # File descriptor: stdout
#         self.assembly.append(f'    mov x1, x0')  # String address from convert_number_to_string
#         self.assembly.append(f'    bl strlen')   # Calculate string length
#         self.assembly.append(f'    mov x2, x0')  # String length
#         self.assembly.append(f'    mov x16, #4') # Syscall: write
#         self.assembly.append(f'    svc 0')
                
#     def _generate_print_string(self, node: dict) -> None:
#         '''
#         Generates assembly to print a string.
#         '''
        
#         literal_label = f'literal_{node.get("asm_literal_label")}'
#         self.assembly.append(f'    adrp x6, {literal_label}@PAGE')
#         self.assembly.append(f'    add x6, x6, {literal_label}@PAGEOFF')
#         self.assembly.append(f'    mov x0, #1')
#         self.assembly.append(f'    mov x1, x6')
#         self.assembly.append(f'    mov x2, #{len(node.get("value"))}')
#         self.assembly.append(f'    mov x16, #4')
#         self.assembly.append(f'    svc 0')
        
                
#     def _generate_intermediate_assignment(self, intermediate_node: dict, var_name: str) -> None:
#         '''
#         Generates an assignment statement for an intermediate expression.
#         '''
#         register_holding_value = intermediate_node.get('name')
        
#         self.assembly.append(f'    adrp x0, {var_name}@PAGE')
#         self.assembly.append(f'    add x0, x0, {var_name}@PAGEOFF')
#         self.assembly.append(f'    str {register_holding_value}, [x0]')
    
                
#     def _generate_binary_expression(self, node: dict) -> dict:
#         '''
#         Adds binary expression operation into the assembly code and
#         returns a new node to be placed in place of the binary expression.
#         '''
        
#         left = node.get('left') 
#         right = node.get('right')
#         operator = node.get('operator')
        
#         # Process left operand
#         if left.get('type') == 'BinaryExpression':
#             left_result = self._generate_binary_expression(left)
#             left_register = left_result.get('name')
#         elif left.get('type') == 'Identifier' or left.get('type') == 'NumericLiteral':
#             left_register = self._load_operand(left, 'x0', 'w1')

#         # Process right operand
#         if right.get('type') == 'BinaryExpression':
#             right_result = self._generate_binary_expression(right)
#             right_register = right_result.get('name')
#         elif right.get('type') == 'Identifier' or right.get('type') == 'NumericLiteral':
#             right_register = self._load_operand(right, 'x2', 'w3')
        
#         # Perform the operation
#         if operator == '+':
#             self.assembly.append(f'    add w5, {left_register}, {right_register}')
#         elif operator == '*':
#             self.assembly.append(f'    mul w5, {left_register}, {right_register}')
#         else:
#             raise ValueError(f'Unsupported operator: {operator}')

#         return {
#             "type": "IntermediateExpression",
#             "name": "w5"
#         }
    
#     def _load_operand(self, node: dict, reg_page: str, reg_offset: str) -> str:
#         '''
#         Loads an operand into a register.
#         Returns the register where the operand is loaded.
#         '''
#         if node.get('type') == 'Identifier':
#             var_name = node.get('name')
#             self.assembly.append(f'    adrp {reg_page}, {var_name}@PAGE')
#             self.assembly.append(f'    add {reg_page}, {reg_page}, {var_name}@PAGEOFF')
#             self.assembly.append(f'    ldr {reg_offset}, [{reg_page}]')
#             return reg_offset
#         elif node.get('type') == 'NumericLiteral':
#             value = node.get('value')
#             self.assembly.append(f'    mov {reg_offset}, #{value}')
#             return reg_offset