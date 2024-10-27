



tokenList = []

# Global index for tracking current token
current_index = 0

# Retrieve the next token in the list
def get_next_token():
    if current_index < len(tokenList):
        return tokenList[current_index]
    return ("", "", -1)

# Move to the next token
def move_to_next():
    global current_index
    current_index += 1

# Check if current token matches expected type
def verify(expected_type):
    print(f"Expected: {expected_type}, Found: {get_next_token().className}")
    if get_next_token().className == expected_type:
        move_to_next()
        return True
    return False

# Program → ClassDeclaration Program
def program():
    if get_next_token().lineNo == -1:
        return True
    if class_declaration():
        if program():
            return True
    return False

# ClassDeclaration → AccessModifier class id Inheritance { ClassContent }
def class_declaration():
    if access_modifier():
        if verify('Class'):
            if verify('id'):
                if inheritance():
                    if verify('{'):
                        if class_content():
                            if verify('}'):
                                return True
    return False

# AccessModifier → public | private | ε
def access_modifier():
    if verify("accMod"):
        return True
    return True  # ε allows absence of access modifier

# Inheritance → extends id | implements id | ε
def inheritance():
    global current_index
    initial_position = current_index
    if get_next_token().className in ['extends', 'implements']:
        if verify(get_next_token().className):
            if verify('id'):
                return True
        return False
    if (initial_position == current_index):
        return True
    return False

# ClassContent → VariableDeclaration ClassContent | FunctionDeclaration ClassContent | ε
def class_content():
    global current_index
    initial_position = current_index
    if variable_declaration():
        if class_content():
            return True
    elif function_declaration():
        if class_content():
            return True
    if (initial_position == current_index):
        return True
    return False

# VariableDeclaration → DT id ;
def variable_declaration():
    if verify('DT'):
        if verify('id'):
            if verify(';'):
                return True
    return False

# FunctionDeclaration → function id ( ParameterList ) Block
def function_declaration():
    if verify('fun'):
        verify('DT')
        if verify('id'):
            if verify('('):
                if parameter_list():
                    if verify(')'):
                        if block():
                            return True
    return False

# ParameterList → DT id AdditionalParams | ε
def parameter_list():
    global current_index
    initial_position = current_index
    if verify('DT'):
        if verify('id'):
            if additional_params():
                return True
    if (initial_position == current_index):
        return True
    return False

# AdditionalParams → , DT id AdditionalParams | ε
def additional_params():
    global current_index
    initial_position = current_index
    if verify(','):
        if verify('DT'):
            if verify('id'):
                if additional_params():
                    return True
    if (initial_position == current_index):
        return True
    return False

# Block → { Statements }
def block():
    if verify('{'):
        if statements():
            if verify('}'):
                return True
    return False

# Statements → Statement Statements | ε
def statements():
    global current_index
    initial_position = current_index
    if statement():
        if statements():
            return True
    if (initial_position == current_index):
        return True
    return False

# Statement → AssignStatement ; | Expression ; | ConditionalStatement | LoopStatement | ReturnStatement ; | VariableDeclaration | FunctionCall ; | Block
def statement():
    if assign_statement():
        if verify(';'):
            return True
    elif expression():
        if verify(';'):
            return True
    elif conditional_statement():
        return True
    elif loop_statement():
        return True
    elif return_statement():
        if verify(';'):
            return True
    elif variable_declaration():
        return True
    elif function_call():
        if verify(';'):
            return True
    elif block():
        return True
    elif until_loop():
        return True
    return False

# AssignStatement → id AssignmentOperator Expression
def assign_statement():
    if verify('id'):
        global current_index
        if assignment_operator():
            if expression():
                return True
        current_index -= 1
    return False

# AssignmentOperator → = | += | -= | *= | /= | %=
def assignment_operator():
    if verify('COMPOP') or verify('='):
        return True
    return False

# ConditionalStatement → if ( Expression ) Statement ElseOption
def conditional_statement():
    if verify('if'):
        if verify('('):
            if expression():
                if verify(')'):
                    if statement():
                        if else_option():
                            return True
    return False

# ElseOption → else Statement | ε
def else_option():
    global current_index
    initial_position = current_index
    if verify('else'):
        if statement():
            return True
    if (initial_position == current_index):
        return True
    return False

# LoopStatement → loop ( Expression ) Statement
def loop_statement():
    if verify('loop'):
        if verify('('):
            if expression():
                if verify(')'):
                    if statement():
                        return True
    return False

# UntilLoop → until ( Initial ; Condition ; Update ) Statement
def until_loop():
    if verify('until'):
        if verify('('):
            if initial():
                if verify(';'):
                    if condition():
                        if verify(';'):
                            if update():
                                if verify(')'):
                                    if statements():
                                        return True
    return False

# Initial → DT id AssignmentOperator Expression | id AssignmentOperator Expression | ε
def initial():
    global current_index
    initial_position = current_index
    if verify('DT'):
        if verify('id'):
            if verify('='):
                if expression():
                    return True
        return False
    elif verify('id'):
        if verify('='):
            if expression():
                return True
        return True
    if (initial_position == current_index):
        return True
    return False

# Condition → Expression | ε
def condition():
    global current_index
    initial_position = current_index
    if expression():
        return True
    if (initial_position == current_index):
        return True
    return False

# Update → assign_statement | assignment_operator expression
def update():
    if assign_statement() or expression():
        return True
    return False

# ReturnStatement → return Expression
def return_statement():
    if verify('ret'):
        if expression():
            return True
    return False

# Expression → RelationalExpression ExpressionTail
def expression():
    if relational_expression():
        if expression_tail():
            return True
    return False

# ExpressionTail → + RelationalExpression ExpressionTail | - RelationalExpression ExpressionTail | ε
def expression_tail():
    global current_index
    initial_position = current_index
    if verify('PM'):
        if relational_expression():
            if expression_tail():
                return True
    if (initial_position == current_index):
        return True
    return False

# RelationalExpression → Term RelationalTail
def relational_expression():
    if term():
        if relational_tail():
            return True
    return False

# RelationalTail → < Term | <= Term | > Term | >= Term | == Term | != Term | ε
def relational_tail():
    global current_index
    initial_position = current_index
    if verify('ROP'):
        if term():
            return True
    if (initial_position == current_index):
        return True
    return False

# Term → Factor TermTail
def term():
    if factor():
        if term_tail():
            return True
    return False

# TermTail → MULTDIVMOD Factor TermTail | ε
def term_tail():
    global current_index
    initial_position = current_index
    if verify('MDM'):
        if factor():
            if term_tail():
                return True
    if (initial_position == current_index):
        return True
    return False

# Factor → PrePostOp? id | intConst | floatConst | FunctionCall | ( Expression ) | PrePostOp? id
def factor():
    global current_index
    if verify("IncDec") and verify('id'):
        return True
    if verify('id'):
        if get_next_token().className == '(':  # Possible function call
            current_index -= 1
            if function_call():
                return True
        if verify("IncDec"):
            return True
        return True
    elif verify('intConst') or verify('floatConst'):
        return True
    elif verify('('):
        if expression():
            if verify(')'):
                return True
    return False

# FunctionCall → id ( Arguments )
def function_call():
    if verify('id'):
        if verify('('):
            if arguments():
                if verify(')'):
                    return True
    return False

# Arguments → Expression AdditionalArgs | ε
def arguments():
    global current_index
    initial_position = current_index
    if expression():
        if additional_args():
            return True
    if (initial_position == current_index):
        return True
    return False

# AdditionalArgs → , Expression AdditionalArgs | ε
def additional_args():
    global current_index
    initial_position = current_index
    if verify(','):
        if expression():
            if additional_args():
                return True
    if (initial_position == current_index):
        return True
    return False

print(program())