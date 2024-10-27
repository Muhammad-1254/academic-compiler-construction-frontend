import re
from src.utils import *


class LexicalAnalyzer:    
    tokens = []
    def __init__(self, code):
        self.source_code = code
        
    def classify_token(self, token):
        if token in keywords:
            return keywords.get(token), token
        elif token in operators:
            return operators.get(token), token
        elif token in punctuators:
            return punctuators.get(token), token
        elif re.match(identifier_re, token):
            return "IDENTIFIER", token
        elif re.match(integer_re, token):
            return "INT_CONSTANT", token
        elif re.match(float_re, token):
            return "FLOAT_CONSTANT", token
        elif re.match(string_re, token):
            return "STRING", token
        else:
            raise Exception("unrecognized Token: ", token)
        
   
    
    def tokenize(self,):
        status =False
        temp = ""
        i =0
        line_number=0
        length = len(self.source_code)
        while i<length:
            char = self.source_code[i]
            # For single line comment
            if char == "#":
                temp =''
                i+=1
                temp_comment = ''
                while self.source_code[i] !="\n":
                    if self.source_code[i+1]=="\n":
                        line_number+=1
                    temp_comment+=self.source_code[i]
                    i+=1
                continue
            # For multi line comment
            if char =="`":
                temp =''
                i+=1
                temp_comment = ''
                if i<length:
                    while self.source_code[i] !="`":
                        temp_comment+=self.source_code[i]
                        i+=1
                        if i<length:
                            if self.source_code[i]=="\n":
                                line_number+=1
                        else:
                            raise Exception("multi line comment not closed")
                    i+=1
                    continue
                    
            
            # For string
            if char == '"':
                temp='"'
                i+=1
                while i<length:
                    char = self.source_code[i]
                    temp+=char
                    if char =="\\":
                        i+=1
                        char = self.source_code[i]
                        temp+=char
                    elif char =='"':
                        break
                    i+=1
                token_type, value = self.classify_token(temp)
                self.tokens.append({"type":token_type,"value":value,})
                temp=""
                i+=1
                continue
            
            # For new line
            if char =="\n":
                if temp:
                    token_type, value = self.classify_token(temp)
                    self.tokens.append({"type":token_type,"value":value,})
                temp=""
                i+=1
                line_number+=1
                continue
            
            # For space and tab
            if char in [" ","\t"]:
                if temp:
                    token_type, value = self.classify_token(temp)
                    self.tokens.append({"type":token_type,"value":value,})
                temp=""
                i+=1
                continue

            # FOR punctuators AND "."
            if char in punctuators:
                if temp:
                    token_type, value = self.classify_token(temp)
                    self.tokens.append({"type":token_type,"value":value,})
                    temp = ""
                if char == ".":
                    status = False
                    if temp:
                        if (not re.match(integer_re, temp)) or (
                            self.source_code[i + 1] not in "1234567890"
                        ):
                            status = True

                        if status == True:
                            token_type, value = self.classify_token(temp)
                            self.tokens.append({"type":token_type,"value":value,})
                            temp = ""
                            status = False
                    elif self.source_code[i + 1] not in "1234567890":
                        status = True

         

            if char in operators:
                if temp:
                    if temp + char not in operators:
                        
                        token_type, value = self.classify_token(temp)
                        self.tokens.append({"type":token_type,"value":value,})
                        temp = ""
                    else:
                        temp += char
                        token_type, value = self.classify_token(temp)
                        self.tokens.append({"type":token_type,"value":value,})
                        temp = ""
                        char = ""

            temp += char

            # FOR OPERATORS
            if (temp in punctuators or temp in operators) and not (
                temp == "." and status == False
            ):
                if i + 1 < length:
                    check = temp + self.source_code[i + 1]
                    if check not in operators:
                        token_type, value = self.classify_token(temp)
                        self.tokens.append({"type":token_type,"value":value,})
                        temp = ""

            i += 1

            # TO CHECK IF THE POINTER HAS REACHED END OF FILE TO THEN TOKENIZE WHATEVER IS IN TEMP
            if i == length:
                if temp:
                    token_type, value = self.classify_token(temp)
                    self.tokens.append({"type":token_type,"value":value,})
        # extra token for notifying end of file
        # self.tokens.append({"type":"EOF","value":"",})
        return self.tokens
    
    def print_tokens(self,):
        for token in self.tokens:
            print(token)

    def save_tokens(self):
        with open("tokens.json", "w") as f:
            f.write(str(self.tokens))
            
            
                
            
            
                