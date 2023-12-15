class CodeGenerator:
    '''
    CodeGenerator is a class that generates assembly code from an AST.
    '''
    
    
    def __init__(self) -> None:
        self.assembly = []
        self.literals_map = {}
        self.literal_count = 0

    def generate(self, ast: dict) -> str:
        self.assembly = []
        self.literal_count = 0
        
        self._generate_entry()
        
        self.assembly.append('.data')
        self._generate_data(ast)
        
        self.assembly.append('\n.text\n_main:')
        self._generate_text(ast)
        
        self._generate_exit()
        
        # Join the sections with appropriate line breaks, adding an extra newline between sections
        formatted_assembly = '\n'.join(self.assembly)
        return formatted_assembly
    
    
    def _generate_entry(self):
        '''
        Appends entry instructions
        '''
        
        entry_instructions = [
            ".global _main",
            ".align 3"
        ]
        
        self.assembly.append(
            "%s\n%s\n" % (
                entry_instructions[0], 
                entry_instructions[1],
            )
        )
    
    def _generate_exit(self):
        '''
        Appends exit syscall to the text section.
        '''

        exit_instructions = [ 
            'mov x0, #0',
            'mov x16, #1',
            'svc 0',
        ]
        
        self.assembly.append(
            '    %s\n    %s\n    %s' % (
                exit_instructions[0], 
                exit_instructions[1], 
                exit_instructions[2]
            )
        )

    def _generate_data(self, node: dict) -> None:
        node_type = node.get('type')

        if node_type == 'Program':
            for child in node.get('body', []):
                self._generate_data(child)

        elif node_type == 'VariableDeclaration':
            for declaration in node.get('declarations', []):
                self._generate_data(declaration)
        
        elif node_type == 'VariableDeclarator':
            var_name = node.get('id').get('name') 
            init = node.get('init')

            if init and init.get('type') == 'NumericLiteral':
                value = init.get('value')
                self.assembly.append(f'    {var_name}: .word {value}')
            elif init and init.get('type') == 'StringLiteral':
                value = init.get('value')
                self.assembly.append(f'    {var_name}: .asciz "{value}"')
            else:
                self.assembly.append(f'    {var_name}: .word 0')

        elif node_type == 'ExpressionStatement':
            self._generate_data(node.get('body'))

        elif node_type == 'BinaryExpression':
            self._generate_data(node.get('left'))
            self._generate_data(node.get('right'))

        elif node_type == 'NumericLiteral':
            if node.get('value') in self.literals_map:
                node['asm_literal_label'] = self.literals_map[node.get('value')]
            else:
                node['asm_literal_label'] = self.literal_count
                self.literals_map[node.get('value')] = self.literal_count
                self.literal_count += 1
                
                literal_label = f'literal_{node.get("asm_literal_label")}'
                value = node.get('value')
                
                self.assembly.append(f'    {literal_label}: .word {value}')

        elif node_type == 'StringLiteral':
            if node.get('value') in self.literals_map:
                node['asm_literal_label'] = self.literals_map[node.get('value')]
            else:
                node['asm_literal_label'] = self.literal_count
                self.literals_map[node.get('value')] = self.literal_count
                self.literal_count += 1
                
                literal_label = f'literal_{node.get("asm_literal_label")}'
                value = node.get('value')
                
                self.assembly.append(f'    {literal_label}: .asciz "{value}"')

        elif node_type == 'CmdPrintStatement':
            self._generate_data(node.get('body'))
    
    def _generate_text(self, node: dict) -> None:
        node_type = node.get('type')

        if node_type == 'Program':
            for child in node.get('body', []):
                self._generate_text(child)
        
        elif node_type == 'ExpressionStatement':
            self._generate_text(node.get('body'))
        
        elif node_type == 'VariableDeclaration':
            for declaration in node.get('declarations', []):
                self._generate_text(declaration)
                
        elif node_type == 'VariableDeclarator':
            var_name = node.get('id').get('name')
            init = node.get('init')

            if init:
                init_type = init.get('type')
                if init_type == 'BinaryExpression':
                    intermediate_node = self._generate_binary_expression(init)
                    self._generate_intermediate_assignment(intermediate_node, var_name)
        
        # Print
        elif node_type == 'CmdPrintStatement':
            self._generate_print(node)
            
    def _generate_print(self, node: dict) -> None:
        '''
        Generates assembly to print a value.
        '''
        
        value = node.get('body')
        if value.get('type') == 'StringLiteral':
            self._generate_print_string(value)
        if value.get('type') == 'NumericLiteral':
            self._generate_print_numeric(value)
                
    def _generate_print_numeric(self, node: dict) -> None:
        '''
        Generates assembly to print a numeric value by converting it to a string.
        '''

        # Assume the numeric value is in w6 and the converted string will be stored starting at address in x7
        # Temporary registers x8 and x9 are used for intermediate calculations
        numeric_label = f'literal_{node.get("asm_literal_label")}'
        self.assembly.append(f'    adrp x6, {numeric_label}@PAGE')
        self.assembly.append(f'    add x6, x6, {numeric_label}@PAGEOFF')
        self.assembly.append(f'    ldr w6, [x6]')

        # Reserve space for the converted string (max 12 bytes for 32-bit int + null terminator)
        self.assembly.append(f'    sub sp, sp, #13')
        self.assembly.append(f'    mov x7, sp')

        # Conversion loop
        self.assembly.append('convert_loop:')
        self.assembly.append(f'    mov w8, #10')
        self.assembly.append(f'    udiv w9, w6, w8')
        self.assembly.append(f'    msub w9, w9, w8, w6')
        self.assembly.append(f'    add w9, w9, #48')  # Convert to ASCII
        self.assembly.append(f'    strb w9, [x7], #1')
        self.assembly.append(f'    mov w6, w9')
        self.assembly.append(f'    cbnz w6, convert_loop')

        # Null-terminate the string
        self.assembly.append(f'    strb wzr, [x7]')

        # Print the string
        self.assembly.append(f'    mov x0, #1')  # File descriptor: stdout
        self.assembly.append(f'    mov x1, sp')  # String address
        self.assembly.append(f'    mov x2, x7')  # String length
        self.assembly.append(f'    sub x2, x2, sp')
        self.assembly.append(f'    mov x16, #4')  # Syscall: write
        self.assembly.append(f'    svc 0')

        # Restore stack pointer
        self.assembly.append(f'    add sp, sp, #13')
                
    def _generate_print_string(self, node: dict) -> None:
        '''
        Generates assembly to print a string.
        '''
        
        literal_label = f'literal_{node.get("asm_literal_label")}'
        self.assembly.append(f'    adrp x6, {literal_label}@PAGE')
        self.assembly.append(f'    add x6, x6, {literal_label}@PAGEOFF')
        self.assembly.append(f'    mov x0, #1')
        self.assembly.append(f'    mov x1, x6')
        self.assembly.append(f'    mov x2, #{len(node.get("value"))}')
        self.assembly.append(f'    mov x16, #4')
        self.assembly.append(f'    svc 0')
        
                
    def _generate_intermediate_assignment(self, intermediate_node: dict, var_name: str) -> None:
        '''
        Generates an assignment statement for an intermediate expression.
        '''
        register_holding_value = intermediate_node.get('name')
        
        self.assembly.append(f'    adrp x0, {var_name}@PAGE')
        self.assembly.append(f'    add x0, x0, {var_name}@PAGEOFF')
        self.assembly.append(f'    str {register_holding_value}, [x0]')
    
                
    def _generate_binary_expression(self, node: dict) -> dict:
        '''
        Adds binary expression operation into the assembly code and
        returns a new node to be placed in place of the binary expression.
        '''
        
        left = node.get('left') 
        right = node.get('right')
        operator = node.get('operator')
        
        # Process left operand
        if left.get('type') == 'BinaryExpression':
            left_result = self._generate_binary_expression(left)
            left_register = left_result.get('name')
        elif left.get('type') == 'Identifier' or left.get('type') == 'NumericLiteral':
            left_register = self._load_operand(left, 'x0', 'w1')

        # Process right operand
        if right.get('type') == 'BinaryExpression':
            right_result = self._generate_binary_expression(right)
            right_register = right_result.get('name')
        elif right.get('type') == 'Identifier' or right.get('type') == 'NumericLiteral':
            right_register = self._load_operand(right, 'x2', 'w3')
        
        # Perform the operation
        if operator == '+':
            self.assembly.append(f'    add w5, {left_register}, {right_register}')
        elif operator == '*':
            self.assembly.append(f'    mul w5, {left_register}, {right_register}')
        else:
            raise ValueError(f'Unsupported operator: {operator}')

        return {
            "type": "IntermediateExpression",
            "name": "w5"
        }
    
    def _load_operand(self, node: dict, reg_page: str, reg_offset: str) -> str:
        '''
        Loads an operand into a register.
        Returns the register where the operand is loaded.
        '''
        if node.get('type') == 'Identifier':
            var_name = node.get('name')
            self.assembly.append(f'    adrp {reg_page}, {var_name}@PAGE')
            self.assembly.append(f'    add {reg_page}, {reg_page}, {var_name}@PAGEOFF')
            self.assembly.append(f'    ldr {reg_offset}, [{reg_page}]')
            return reg_offset
        elif node.get('type') == 'NumericLiteral':
            value = node.get('value')
            self.assembly.append(f'    mov {reg_offset}, #{value}')
            return reg_offset