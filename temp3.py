from lexical_anaylizer import tokenList, Token
from collections import defaultdict

# Global token index to track the current token
current_token_index = 0

# Argument counter for tracking function arguments
argCount = 0

# Class to manage scope and symbols during semantic analysis
class SemanticAnalyzer:
    def _init_(self):
        self.symbolTable = defaultdict(dict)  # Stores symbols with type and scope info
        self.scopeStack = [1]  # Stack to manage current scopes
        self.param_count = {}  # Tracks function parameter counts
        self.scopeNo = 2  # Scope number tracker
        self.errors = []  # List of semantic errors

    def current_scope(self):
        return self.scopeStack[-1]

    def enter_scope(self):
        self.scopeStack.append(self.scopeNo)
        self.scopeNo += 1

    def exit_scope(self):
        if len(self.scopeStack) > 1:
            self.scopeStack.pop()
            self.scopeNo -= 1
            self.symbolTable[self.scopeNo].clear()

    def declare_variable(self, name, data_type, lineNo):
        scope = self.current_scope()
        if name not in self.symbolTable[scope]:
            self.symbolTable[scope][name] = {"type": data_type, "scope": scope}
        else:
            self.errors.append(f"Semantic Error: '{name}' redeclared on line {lineNo}")

    def declare_function(self, name, param_types):
        self.param_count[name] = len(param_types)

    def lookup_variable(self, name):
        for scope in reversed(self.scopeStack):
            if name in self.symbolTable[scope]:
                return True
        return False

    def lookup_function(self, name):
        for scope in reversed(self.scopeStack):
            if name in self.symbolTable[scope] and self.symbolTable[scope][name]['type'] == 'fun':
                return True
        return False

    def lookup_class(self, name):
        for scope in reversed(self.scopeStack):
            if name in self.symbolTable[scope] and self.symbolTable[scope][name]['type'] == 'class':
                return True
        return False

    def var_type(self, name):
        for scope in reversed(self.scopeStack):
            if name in self.symbolTable[scope]:
                return self.symbolTable[scope][name]['type']
        return None

    def check_function_call(self, name, actual_args_count, lineNo):
        if name in self.param_count:
            expected_args_count = self.param_count[name]
            if actual_args_count != expected_args_count:
                self.errors.append(
                    f"Semantic Error: Function '{name}' expected {expected_args_count} arguments but got {actual_args_count} on line {lineNo}"
                )

    def report_errors(self):
        for error in self.errors:
            print(error)
        if not self.errors:
            print("No semantic errors found.")

# Instantiate the semantic analyzer
semantic_analyzer = SemanticAnalyzer()

# Token navigation functions
def next_token():
    if current_token_index < len(tokenList):
        return tokenList[current_token_index]
    return Token("", "", -1)

def advance():
    global current_token_index
    current_token_index += 1

def match(expected_value):
    if next_token().className == expected_value:
        advance()
        return True
    return False

# Grammar rules and parsing functions
def program():
    if next_token().lineNo == -1:
        return True
    if class_decl():
        if program():
            return True
    return False

def class_decl():
    if access_modifier():
        if match('Class') and match('id'):
            class_name = tokenList[current_token_index - 1].value
            lineNo = tokenList[current_token_index - 1].lineNo
            semantic_analyzer.declare_variable(class_name, 'class', lineNo)
            semantic_analyzer.enter_scope()
            if inheritance() and match('{') and class_body() and match('}'):
                semantic_analyzer.exit_scope()
                return True
    return False

def access_modifier():
    return match("accMod") or True

def inheritance():
    index = current_token_index
    if next_token().className in ['extends', 'implements']:
        if match(next_token().className) and match('id'):
            class_name = tokenList[current_token_index - 1].value
            lineNo = tokenList[current_token_index - 1].lineNo
            if not semantic_analyzer.lookup_class(class_name):
                semantic_analyzer.errors.append(f"Semantic Error: Undeclared class '{class_name}' on line {lineNo}")
            return True
        return False
    return current_token_index == index

def class_body():
    index = current_token_index
    if var_decl() or func_decl():
        return class_body()
    return current_token_index == index

def var_decl():
    if match('DT'):
        data_type = tokenList[current_token_index - 1].value
        if match('id'):
            var_name = tokenList[current_token_index - 1].value
            lineNo = tokenList[current_token_index - 1].lineNo
            semantic_analyzer.declare_variable(var_name, data_type, lineNo)
            if match(';'):
                return True
    return False

def func_decl():
    if match('fun'):
        match('DT')
        if match('id'):
            func_name = tokenList[current_token_index - 1].value
            lineNo = tokenList[current_token_index - 1].lineNo
            param_types = []
            semantic_analyzer.declare_variable(func_name, "fun", lineNo)
            semantic_analyzer.enter_scope()
            if match('(') and param_list(param_types) and match(')') and block():
                semantic_analyzer.exit_scope()
                semantic_analyzer.declare_function(func_name, param_types)
                return True
    return False

def param_list(param_types):
    index = current_token_index
    if match('DT'):
        data_type = tokenList[current_token_index - 1].value
        if match('id'):
            param_name = tokenList[current_token_index - 1].value
            lineNo = tokenList[current_token_index - 1].lineNo
            semantic_analyzer.declare_variable(param_name, data_type, lineNo)
            param_types.append(data_type)
            return more_params(param_types)
    return current_token_index == index

def more_params(param_types):
    index = current_token_index
    if match(',') and match('DT'):
        data_type = tokenList[current_token_index - 1].value
        if match('id'):
            param_name = tokenList[current_token_index - 1].value
            lineNo = tokenList[current_token_index - 1].lineNo
            semantic_analyzer.declare_variable(param_name, data_type, lineNo)
            param_types.append(data_type)
            return more_params(param_types)
    return current_token_index == index

def block():
    if match('{'):
        semantic_analyzer.enter_scope()
        if stmts() and match('}'):
            semantic_analyzer.exit_scope()
            return True
    return False

def stmts():
    index = current_token_index
    if stmt():
        return stmts()
    return current_token_index == index

def stmt():
    if assign_stmt() or expr() or if_stmt() or loop_stmt() or return_stmt() or var_decl() or func_call() or block():
        return match(';')
    return False

def assign_stmt():
    if match('id'):
        var_name = tokenList[current_token_index - 1].value
        lineNo = tokenList[current_token_index - 1].lineNo
        if assign_op():
            if not semantic_analyzer.lookup_variable(var_name):
                semantic_analyzer.errors.append(f"Semantic Error: Undeclared variable '{var_name}' on line {lineNo}")
            if expr():
                return True
    return False

def assign_op():
    return match('COMPOP') or match('=')

def if_stmt():
    return match('if') and match('(') and expr() and match(')') and stmt() and else_opt()

def else_opt():
    return match('else') and stmt() or True

def loop_stmt():
    return match('loop') and match('(') and expr() and match(')') and stmt()

def return_stmt():
    return match('ret') and expr()

def expr():
    return rel_expr() and expr_tail()

def expr_tail():
    return match('PM') and rel_expr() and expr_tail() or True

def rel_expr():
    return term() and rel_expr_tail()

def rel_expr_tail():
    return match('ROP') and term() or True

def term():
    return factor() and term_tail()

def term_tail():
    return match('MDM') and factor() and term_tail() or True

def factor():
    return match("IncDec") and match('id') or match('id') or match('intConst') or match('floatConst') or match('(') and expr() and match(')')

def func_call():
    if match('id') and match('('):
        global argCount
        argCount = 0
        if args() and match(')'):
            func_name = tokenList[current_token_index - 1].value
            lineNo = tokenList[current_token_index - 1].lineNo
            if not semantic_analyzer.lookup_function(func_name):
                semantic_analyzer.errors.append(f"Semantic Error: Undeclared function '{func_name}' on line {lineNo}")
            semantic_analyzer.check_function_call(func_name, argCount, lineNo)
            return True
    return False

def args():
    index = current_token_index
    global argCount
    if expr():
        argCount += 1
        return more_args()
    return current_token_index == index

def more_args():
    index = current_token_index
    global argCount
    if match(','):
        if expr():
            argCount += 1
            return more_args()
    return current_token_index == index


# Start parsing from the program and check for semantic errors
print("Parsing result:", program())
semantic_analyzer.report_errors()