import sys
from csci4342_Part1 import tokenator, parse as lex_parse

def parse(tokens):
    global current_token, token_index
    token_index = -1
    current_token = None

    def advance():
        global current_token, token_index
        token_index += 1
        if token_index < len(tokens):
            current_token = tokens[token_index]
        else:
            current_token = None

    def match(expected_type, expected_value=None):
        if not current_token:
            raise SyntaxError(f"Expected {expected_type}, got end of input")
        if current_token[1] != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {current_token[1]}")
        if expected_value is not None and current_token[0] != expected_value:
            raise SyntaxError(f"Expected '{expected_value}', got '{current_token[0]}'")
        advance()

    def program():
        match("Reserved Token", "program") 
        match("Identifier Token")         
        match("Special Token", ";") 
        block()
        match("Special Token", ".")     

    def block():
        variable_declaration_part()
        procedure_declaration_part()
        statement_part()

    def variable_declaration_part():
        if not current_token: #ensures that we aren't at the end of the input stream 
            return  
        match("Reserved Token", "var")
        variable_declaration_list()

    def variable_declaration_list():
        variable_declaration()
        while current_token:
            if current_token[0] != ";":
                break
            match("Special Token", ";")
            variable_declaration()

    def variable_declaration():
        identifier_list()
        match("Special Token", ":")    
        type_token()

    def identifier_list():
        match("Identifier Token")
        while current_token:
            if current_token[0] != ",":
                break
            match("Special Token", ",")
            match("Identifier Token")

    def type_token():
        simple_type()
        
    def simple_type():
        if current_token[0] == "integer":
            match("Data Type Token", "integer")
        elif current_token[0] == "boolean":
            match("Data Type Token", "boolean")
        else:
            raise SyntaxError(f"Expected 'integer' or 'boolean', got {current_token[0]}")
    
    def procedure_declaration_part():
        procedure_declaration_list()
        
    def procedure_declaration_list():
        procedure_declaration()
        while current_token:
            if current_token[0] != ";":
                break
            match("Special Token", ";")
            procedure_declaration()
        
    def procedure_declaration():
        match("Reserved Token", "procedure")
        match("Identifier Token")
        match("Special Token", ";")
        procedure_block()
        
    def procedure_block():
        variable_declaration_part()
        statement_part()

    def statement_part():
        compound_statement()
    
    def compound_statement():
        match("Reserved Token", "begin")
        statement_list()
        match("Reserved Token", "end")
        
    def statement_list():
        while current_token and current_token[0] != "end":
            statement()

    def statement():
        if is_simple_statement():
            simple_statement()
        else:
            structured_statement()
    
    def is_simple_statement(): # simple statements either begin with read/write or have an identifier token
        return (current_token and (current_token[1] == "Identifier Token" or current_token[0] in ["read", "write"])) 
    
    def simple_statement():
        if current_token[1] == "Identifier Token":
            if current_token[2] and current_token[3] == ":=":
                assignment_statement()
            else:
                procedure_statement()
        elif current_token[0] == "read":
            read_statement()
        elif current_token[0] == "write":
            write_statement()
        else:
            raise SyntaxError("Invalid simple statement")
    
    def assignment_statement():
        variable()
        match("Assignment Token")
        expression()
    
    def procedure_statement():
        procedure_identifier()
    
    def procedure_identifier():
        match("Identifier Token")
    
    def read_statement():
        match("Reserved Token", "read")
        input_variable()
    
    def input_variable():
        variable()
        
    def write_statement():
        match("Reserved Token", "write")
        output_value()
    
    def output_value():
        expression()
    
    def structured_statement():
        if current_token[0] == "if":
            if_statement()
        elif current_token[0] == "while":
            while_statement()
        else:
            compound_statement()
    
    def if_statement():
        match("Reserved Token", "if")
        expression()
        match("Reserved Token", "then")
        statement()
        if match("Reserved Token", "else"):
            statement()
            
    def while_statement():
        match("Reserved Token", "while")
        expression()
        match("Reserved Token", "do")
        statement()
        
    def expression():
        simple_expression()
        if match("Relation Token"):
            simple_expression()
    
    def simple_expression():
        term()
        addition_operations_list()
        
    def term():
        factor()
        multiplication_operations_list()
    
    def factor():
           
    
    # Start the parsing process
    advance()
    program()

def main():
    if len(sys.argv) != 2:
        print("Usage: python parser.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as file:
        content = file.read()

    tokens = []
    for line in content.split('\n'):
        tokens.extend(lex_parse(line))

    try:
        parse(tokens)
        print("Parsing successful!")
    except SyntaxError as e:
        print(f"Parsing error: {e}")

if __name__ == "__main__":
    main()