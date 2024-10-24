from src.lexical_analyzer import LexicalAnalyzer
if __name__ =='__main__':
    code_file  = open('test_code.myLang', 'r')
    code = code_file.read()
    lexicalAnalyzer = LexicalAnalyzer(code)
    lexicalAnalyzer.tokenize()
    lexicalAnalyzer.print_tokens()
    