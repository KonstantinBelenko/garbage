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

            if init and init.get('type') == 'BinaryExpression':
                self._generate_binary_expression(init, var_name)
                
    def _generate_binary_expression(self, node: dict, result_var: str) -> None:
        left = node.get('left')
        right = node.get('right')
        
        left_var = left.get('name')
        right_var = right.get('name')
        
        # Load left variable into a register
        self.assembly.append(f'    adrp x1, {left_var}@PAGE')
        self.assembly.append(f'    add x1, x1, {left_var}@PAGEOFF')
        self.assembly.append(f'    ldr w2, [x1]')
        
        # Load right variable into a register
        self.assembly.append(f'    adrp x3, {right_var}@PAGE')
        self.assembly.append(f'    add x3, x3, {right_var}@PAGEOFF')
        self.assembly.append(f'    ldr w4, [x3]')
        
        # Perform addition
        self.assembly.append('    add w2, w2, w4')

        # Store the result in the result variable
        self.assembly.append(f'    adrp x5, {result_var}@PAGE')
        self.assembly.append(f'    add x5, x5, {result_var}@PAGEOFF')
        self.assembly.append(f'    str w2, [x5]')
        