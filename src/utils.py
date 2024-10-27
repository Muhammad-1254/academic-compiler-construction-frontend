 
identifier_re = r"[a-zA-Z_][a-zA-Z0-9_]*"
integer_re = r"^[+-]?\d+$"
float_re = r"^[+-]?(\d*\.\d+|\d+\.\d*)([eE][+-]?\d+)?$"
string_re = r"\".*\""


keywords = {
    # oop related keywords
    "class": "CLASS",
    "abstract": "ABSTRACT",
    "public": "PUBLIC",
    "interface": "INTERFACE",
    "extends": "EXTENDS",
    "instanceof": "INSTANCEOF",
    "super": "SUPER",
    "new": "NEW",
    "this": "THIS",
    # data mutability related keywords
    "const": "CONST",
    "var": "VAR",
    # data types
    "boolean": "BOOLEAN",
    "int": "INT",
    "float": "FLOAT",
    "any": "ANY",
    "string": "STRING",
    # loop related keywords
    "while": "WHILE",
    "do": "DO",
    "for": "FOR",
    "continue": "CONTINUE",
    "break": "BREAK",
    # conditional statements related keywords
    "if": "IF",
    "else": "ELSE",
    # function related keywords
    # "function or def",
    "function": "FUNCTION",
    "def": "DEF",
    "void": "VOID",
    "return": "RETURN",
    # error handling related keywords
    "throw": "THROW",
    "catch": "CATCH",
}

operators = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "%": "MODULUS",
    "++": "INC",
    "--": "DEC",
    "=": "ASSIGN",
    "+=": "INC_ASSIGN",
    "-=": "DEC_ASSIGN",
    "/=": "DIV_ASSIGN",
    "*=": "MUL_ASSIGN",
    "%=": "MOD_ASSIGN",
    "==": "EQ",
    "!=": "NEQ",
    "<=": "LE",
    ">=": "GE",
    "<": "LT",
    ">": "GT",
    "&&": "AND",
    "||": "OR",
    "!": "NOT",
}


punctuators = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    "[": "LBRACKET",
    "]": "RBRACKET",
    ";": "SEMICOLON",
    ",": "COMMA",
    ".": "DOT",
}
