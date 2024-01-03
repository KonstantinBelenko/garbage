from src.parser import ASTParser, NT, Node
import unittest

if 'unittest.util' in __import__('sys').modules:
    # Show full diff in self.assertEqual.
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

class TestFunctionDeclaration(unittest.TestCase):
    
    def setUp(self):
        self.ast_parser = ASTParser()
        self.maxDiff = None
    
    def test_(self):
        pass


if __name__ == '__main__':
    unittest.main()