class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDeclNode(ASTNode):
    def __init__(self, var_type, identifier, expression):
        self.var_type = var_type
        self.identifier = identifier
        self.expression = expression

class AssignmentNode(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class PrintNode(ASTNode):
    def __init__(self, identifier):
        self.identifier = identifier

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

class LL1Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
    
    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = {"type": "EOF", "value": ""}

    def match(self, expected_type):
        if self.current_token["type"] == expected_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {expected_type}, but found {self.current_token['type']}")

    def parse(self):
        program_node = self.program()
        if self.current_token["type"] != "EOF":
            raise SyntaxError("Unexpected token at end of program")
        return program_node
    
    def program(self):
        statements = self.statements()
        return ProgramNode(statements)

    def statements(self):
        statements = []
        while self.current_token["type"] in {"INT", "IDENTIFIER", "PRINT"}:
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token["type"] == "INT":
            return self.var_decl()
        elif self.current_token["type"] == "IDENTIFIER":
            return self.assignment()
        elif self.current_token["type"] == "PRINT":
            return self.print_stmt()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token['type']} in statement")

    def var_decl(self):
        self.match("INT")
        identifier = self.current_token["value"]
        self.match("IDENTIFIER")
        self.match("ASSIGN")
        expression = self.expression()
        self.match("SEMICOLON")
        return VarDeclNode("int", identifier, expression)

    def assignment(self):
        identifier = self.current_token["value"]
        self.match("IDENTIFIER")
        self.match("ASSIGN")
        expression = self.expression()
        self.match("SEMICOLON")
        return AssignmentNode(identifier, expression)

    def print_stmt(self):
        self.match("PRINT")
        self.match("LPAREN")
        identifier = self.current_token["value"]
        self.match("IDENTIFIER")
        self.match("RPAREN")
        self.match("SEMICOLON")
        return PrintNode(identifier)

    def expression(self):
        term_node = self.term()
        return self.expression_prime(term_node)

    def expression_prime(self, left):
        if self.current_token["type"] in {"PLUS", "MINUS"}:
            operator = self.current_token["type"]
            self.advance()
            right = self.term()
            left = BinaryOpNode(left, operator, right)
            return self.expression_prime(left)
        return left

    def term(self):
        factor_node = self.factor()
        return self.term_prime(factor_node)

    def term_prime(self, left):
        if self.current_token["type"] in {"MUL", "DIV"}:
            operator = self.current_token["type"]
            self.advance()
            right = self.factor()
            left = BinaryOpNode(left, operator, right)
            return self.term_prime(left)
        return left

    def factor(self):
        if self.current_token["type"] == "NUMBER":
            value = int(self.current_token["value"])
            self.match("NUMBER")
            return NumberNode(value)
        elif self.current_token["type"] == "IDENTIFIER":
            name = self.current_token["value"]
            self.match("IDENTIFIER")
            return IdentifierNode(name)
        elif self.current_token["type"] == "LPAREN":
            self.match("LPAREN")
            expr_node = self.expression()
            self.match("RPAREN")
            return expr_node
        else:
            raise SyntaxError(f"Unexpected token {self.current_token['type']} in factor")

# Example token stream
tokens = [
    {"type": "INT", "value": "int"},
    {"type": "IDENTIFIER", "value": "a"},
    {"type": "ASSIGN", "value": "="},
    {"type": "NUMBER", "value": "0"},
    {"type": "SEMICOLON", "value": ";"},
    {"type": "INT", "value": "int"},
    {"type": "IDENTIFIER", "value": "b"},
    {"type": "ASSIGN", "value": "="},
    {"type": "NUMBER", "value": "3"},
    {"type": "SEMICOLON", "value": ";"},
    {"type": "INT", "value": "int"},
    {"type": "IDENTIFIER", "value": "z"},
    {"type": "ASSIGN", "value": "="},
    {"type": "IDENTIFIER", "value": "a"},
    {"type": "PLUS", "value": "+"},
    {"type": "IDENTIFIER", "value": "b"},
    {"type": "SEMICOLON", "value": ";"},
    {"type": "EOF", "value": ""}
]

# Instantiate and run the parser
from src.lexical_analyzer import LexicalAnalyzer
code_file  = open('test_code.myLang', 'r')
code = code_file.read()
lexicalAnalyzer = LexicalAnalyzer(code)
tokens = lexicalAnalyzer.tokenize()
lexicalAnalyzer.print_tokens()
parser = LL1Parser(tokens)
ast = parser.parse()
# save this ast to a file
# print(ast)
import json
with open('ast.json', 'w') as f:
    f.write(json.dumps(ast, default=lambda x: x.__dict__, indent=2))
