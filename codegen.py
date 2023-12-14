class CodeGenerator:
    '''
    CodeGenerator is a class that generates assembly code from an AST.
    '''
    
    
    def __init__(self) -> None:
        self.assembly = []
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

        elif node_type == 'ExpressionStatement':
            self._generate_data(node.get('body'))

        elif node_type == 'NumericLiteral':
            literal_label = f'literal_{self.literal_count}'
            self.literal_count += 1
            value = node.get('value')
            self.assembly.append(f'    {literal_label}: .word {value}')
    
    def _generate_text(self, node: dict) -> None:
        node_type = node.get('type')

        # if node_type == 'Program':
        #     for child in node.get('body', []):
        #         self._generate(child)
        # elif node_type == 'ExpressionStatement':
        #     self._generate(node.get('body'))
        # elif node_type == 'NumericLiteral':
        #     literal_label = f'literal_{self.literal_count}'
        #     self.literal_count += 1
        #     value = node.get('value')
        #     # Ensure proper indentation for literals in the data section
        #     self.data_section.append(f'    {literal_label}: .word {value}')
    