from src.lexical_analyzer import LexicalAnalyzer
from src.syntax_analyzer import SyntaxAnalyzer
if __name__ =='__main__':
    code_file  = open('test_code.myLang', 'r')
    code = code_file.read()
    lexicalAnalyzer = LexicalAnalyzer(code)
    tokens = lexicalAnalyzer.tokenize()
    lexicalAnalyzer.print_tokens()
    syntaxAnalyzer = SyntaxAnalyzer(tokens)
    try:
        
        ast = syntaxAnalyzer.parse()
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    
    