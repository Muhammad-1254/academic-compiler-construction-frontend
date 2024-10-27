class ASTNode:
    """Base class for all AST nodes."""

    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.children = children or []
        self.value = value

    # def __repr__(self):
    #     return f"{self.node_type}({self.value}, {self.children})"


class ClassNode(ASTNode):
    def __init__(self, name, children=None):
        super().__init__("Class", children)
        self.name = name


class InterfaceNode(ASTNode):
    def __init__(self, name, children=None):
        super().__init__("Interface", children)
        self.name = name


class MethodNode(ASTNode):
    def __init__(self, name, params=None, body=None):
        super().__init__("Method", body)
        self.name = name
        self.params = params or []


class StatementNode(ASTNode):
    def __init__(self, statement_type, expression=None):
        super().__init__("Statement")
        self.statement_type = statement_type
        self.expression = expression


class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def advance(self):
        """Advance to the next token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]

    def consume(self, token_type):
        """Consume a token if it matches the expected type."""
        if self.current_token["type"] == token_type:
            value = self.current_token["value"]
            self.advance()
            return value
        else:
            raise SyntaxError(
                f"Expected {token_type}, found {self.current_token['type']}"
            )

    def parse(self):
        """Start parsing and build the AST."""
        ast = ASTNode("Program")
        while self.current_token_index < len(self.tokens):
            if self.current_token["type"] in ("PUBLIC", "PRIVATE"):
                self.advance()
            elif self.current_token["type"] == "CLASS":
                ast.children.append(self.parse_class())
            elif self.current_token["type"] == "INTERFACE":
                ast.children.append(self.parse_interface())
            else:
                ast.children.append(self.parse_statement())
        return ast

    def parse_class(self):
        """Parse a class declaration."""
        self.consume("CLASS")
        class_name = self.consume("IDENTIFIER")
        class_node = ClassNode(name=class_name)

        if self.current_token["type"] == "EXTENDS":
            self.advance()
            class_node.children.append(
                ASTNode("Extends", value=self.consume("IDENTIFIER"))
            )
        if self.current_token["type"] == "IMPLEMENTS":
            self.advance()
            class_node.children.append(
                ASTNode("Implements", value=self.consume("IDENTIFIER"))
            )

        self.consume("LBRACE")
        while self.current_token["type"] != "RBRACE":
            class_node.children.append(self.parse_member())
        self.consume("RBRACE")
        return class_node

    def parse_interface(self):
        """Parse an interface declaration."""
        self.consume("INTERFACE")
        interface_name = self.consume("IDENTIFIER")
        interface_node = InterfaceNode(name=interface_name)

        self.consume("LBRACE")
        while self.current_token["type"] != "RBRACE":
            interface_node.children.append(self.parse_method_signature())
        self.consume("RBRACE")
        return interface_node

    def parse_member(self):
        """Parse a class member, which can be a method or a constant."""
        # TODO: add other types of class members
        if self.current_token["type"] == "CONST":
            self.advance()
            const_type = self.consume("INT")
            const_name = self.consume("IDENTIFIER")
            self.consume("ASSIGN")
            value = self.consume("NUMBER")
            self.consume("SEMICOLON")
            return ASTNode(
                "Constant",
                value={"type": const_type, "name": const_name, "value": value},
            )
        elif self.current_token["type"] in (
            "VOID",
            "INT",
            "IDENTIFIER",
            "PUBLIC",
            "PRIVATE",
        ):
            return self.parse_method_signature()
        else:
            raise SyntaxError(
                f"Unexpected token in class member: {self.current_token['type']}"
            )

    def parse_method_signature(self):
        """Parse a method signature."""
        return_type = self.current_token["type"]
        if return_type == "VOID":
            self.consume("VOID")
        elif return_type == "INT":
            self.consume("INT")
        elif return_type == "IDENTIFIER":
            self.consume("IDENTIFIER")

        method_name = self.consume("IDENTIFIER")
        method_node = MethodNode(name=method_name)

        self.consume("LPAREN")
        params = []

        def parse_params():
            if self.current_token["type"] in (
                "INT",
                "FLOAT",
                "STRING",
                "BOOLEAN",
                "ANY",
                "IDENTIFIER",
            ):
                param_type = self.consume(self.current_token["type"])
                param_name = self.consume("IDENTIFIER")
                params.append((param_type, param_name))

        if self.current_token["type"] != "RPAREN":
            parse_params()
        while self.current_token["type"] == "COMMA":
            self.consume("COMMA")
            if self.tokens[self.current_token_index]["type"] != "RPAREN":
                parse_params()
        method_node.params = params
        self.consume("RPAREN")

        if self.current_token["type"] == "LBRACE":
            self.consume("LBRACE")
            method_body = []
            while self.current_token["type"] != "RBRACE":
                method_body.append(self.parse_statement())
            method_node.children = method_body
            self.consume("RBRACE")
        else:
            self.consume("SEMICOLON")

        return method_node

    def parse_statement(self):
        """Parse a single statement."""
        if (
            self.current_token["type"] == "IDENTIFIER"
            and self.tokens[self.current_token_index + 1]["type"] == "LPAREN"
        ):
            return self.parse_method_call()
        elif self.current_token["type"] in ("INT", "FLOAT", "STRING", "BOOLEAN", "ANY"):
            return self.parse_variable_assign_or_declaration()

        else:
            raise SyntaxError(
                f"Unexpected statement type: {self.current_token['type']}"
            )

    def parse_variable_assign_or_declaration(self):
       
        # for A a = new A();
        if self.current_token['type'] == "IDENTIFIER" and self.tokens[self.current_token_index+1]['type'] == "IDENTIFIER":
            var_type = self.consume("IDENTIFIER")
            var_name = self.consume("IDENTIFIER")
            self.consume("ASSIGN")
            # for instance of class
            if self.current_token['type'] == "NEW":
                self.consume("NEW")
                expression = self.consume("IDENTIFIER")
                self.consume("LPAREN")
                # parse arguments
                args = []
                if self.current_token["type"] in (
                    "INT",
                    "FLOAT",
                    "STRING",
                    "BOOLEAN",
                    "ANY",
                    "IDENTIFIER",
                ):
                    args.append(self.consume(self.current_token["type"]))
                    while self.current_token["type"] == "COMMA":
                        self.consume("COMMA")
                        args.append(self.consume(self.current_token["type"]))
                self.consume("RPAREN")
                self.consume("SEMICOLON")
            return StatementNode("DeclarationAssignment",expression={"type":var_type, "name":var_name, "value":expression, "args":args})
           
        # for int a = 0;, int a,b,c=3;
        elif self.current_token['type'] in("INT", "FLOAT", "STRING", "BOOLEAN", "ANY")  and self.tokens[self.current_token_index+1]['type']=='IDENTIFIER':
            
            var_type = self.consume(self.current_token['type'])
            var_name = self.consume("IDENTIFIER")
            if self.current_token['type'] =="ASSIGN":
                self.consume("ASSIGN")
                value = self.consume(self.current_token['type'])
                self.consume("SEMICOLON")
                return StatementNode("DeclarationAssignment",expression={"type":var_type,"name":var_name, "value":value, })
            elif self.current_token['type'] == "COMMA":
                statements = [{"type":var_type,"name":var_name}]
                self.consume("COMMA")
                while self.current_token['type'] != "ASSIGN":
                    var_name = self.consume("IDENTIFIER")
                    if self.current_token['type'] == "COMMA":
                        self.consume("COMMA")
                    statements.append({"type":var_type,"name":var_name})
                self.consume("ASSIGN")
                if self.current_token['type'] in ("INT_CONSTANT", "FLOAT_CONSTANT", "STRING", "BOOLEAN", "ANY", "IDENTIFIER"):
                    value = self.consume(self.current_token['type'])
                    self.consume("SEMICOLON")
                    statements = [{"type":var_type,"name":var_name, "value":value} for var_name in statements]   
                else:
                    raise SyntaxError(f"Invalid assignment: {self.current_token['type']}")
                return StatementNode("DeclarationAssignment",expression=statements)
                
            elif self.current_token['type'] == "SEMICOLON":
                self.consume("SEMICOLON")
            else:
                raise SyntaxError("Invalid variable declaration or assignment syntax.")
        
        # for a=SOME_VALUE;
        elif self.current_token['type'] == 'IDENTIFIER' and self.tokens[self.current_token_index+1]['type']=='ASSIGN':
            var_name = self.consume("IDENTIFIER") 
            self.consume("ASSIGN")
            if self.current_token['type'] in ("INT_CONSTANT", "FLOAT_CONSTANT", "STRING", "BOOLEAN", "ANY", "IDENTIFIER"):
                value = self.consume(self.current_token['type'])
                self.consume("SEMICOLON") 
                return StatementNode("Assignment",expression={"name":var_name, "value":value})
            else:
                raise SyntaxError(f"Invalid assignment: {self.current_token['type']}")
        else:
            raise SyntaxError(f"Invalid variable declaration or assignment syntax: {self.current_token['type']}")
    def parse_expression(self):
        pass
    

    def parse_method_call(self):
        method_name = self.consume("IDENTIFIER")
        if self.current_token["type"] == "LPAREN":
            self.consume("LPAREN")
            # Parsing arguments
            args = []
            if self.current_token["type"] in (
                "INT_CONSTANT",
                "FLOAT_CONSTANT",
                "STRING",
                "BOOLEAN",
                "IDENTIFIER",
            ):
                args.append(self.consume(self.current_token["type"]))
                while self.current_token["type"] == "COMMA":
                    self.consume("COMMA")
                    if self.current_token["type"] in (
                        "INT",
                        "FLOAT",
                        "STRING",
                        "BOOLEAN",
                        "ANY",
                        "IDENTIFIER",
                    ):
                        args.append(self.consume(self.current_token["type"]))
            self.consume("RPAREN")
            self.consume("SEMICOLON")
            return StatementNode(
                "MethodCall", expression={"name": method_name, "args": args}
            )
        else:
            raise SyntaxError("Invalid assignment or method call syntax.")



if __name__ == '__main__':
    file = open("test_code.myLang", "r")
    code = file.read()
    from src.lexical_analyzer import LexicalAnalyzer

    lexer = LexicalAnalyzer(code)
    tokens = lexer.tokenize()
    lexer.save_tokens()
    lexer.print_tokens()
    parser = SyntaxAnalyzer(tokens)

    ast = parser.parse()
    import json

    with open("ast.json", "w") as f:
        f.write(json.dumps(ast, indent=4, default=lambda x: x.__dict__))
