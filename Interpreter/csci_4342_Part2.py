import sys
import re

# Lexical Analyzer definitions
special_keyword = ['not', 'if', 'then', 'else', 'of', 'while', 'do', 'begin', 'end', 'read', 'write', 'var', 'array', 'procedure', 'program']
special_char = ['|', '.', ',', ';', ':', '..', '(', ')']
assignment_operator = ':='
relational_operator = ['=', '<>', '<', '<=', '>=', '>']
adding_operator = ['+', '-', 'or']
multiplying_operator = ['*', 'div', 'and']
predefined_identifier = ['integer', 'boolean', 'true', 'false']

# Global variables for parser
tokens = []
current_token = None
token_index = 0

def tokenator(token):
    if token in special_keyword:
        return "Reserved Token"
    elif token in predefined_identifier:
        return "Data Type Token"
    elif token in relational_operator:
        return "Relation Token"
    elif token == assignment_operator:
        return "Assignment Token"
    elif token in adding_operator:
        return "Addition Token"
    elif token in multiplying_operator:
        return "Multiplication Token"
    elif token.isdigit():
        return "Integer Token"
    elif re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', token):
        return "Identifier Token"
    elif token in special_char:
        return "Special Token"
    else:
        return "Invalid Token"

def parse(filehandle):
    global tokens, current_token, token_index
    token_regex = re.compile(r'(\w+|\:=|<=|>=|<>|[^\w\s])')
    tokens = []
    for line in filehandle:
        line = line.strip()
        line_tokens = token_regex.findall(line)
        for token in line_tokens:
            token_type = tokenator(token)
            tokens.append((token, token_type))
    
    token_index = 0
    current_token = tokens[0] if tokens else None
    
    # Start parsing
    program()

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
    if current_token[1] != expected_type and current_token[1] not in [
        "Addition Token",
        "Multiplication Token",
        "Relation Token",
        "Integer Token",
        "Data Type Token"
    ]:
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
    if current_token and current_token[0] == "var":
        match("Reserved Token", "var")
        variable_declaration()
        match("Special Token", ";")
        while current_token and current_token[1] == "Identifier Token":
            variable_declaration()
            match("Special Token", ";")

def variable_declaration():
    match("Identifier Token")
    while current_token and current_token[0] == ",":
        match("Special Token", ",")
        match("Identifier Token")
    match("Special Token", ":")
    simple_type()

def simple_type():
    if current_token[0] in ["integer", "boolean"]:
        match("Data Type Token")
    else:
        raise SyntaxError(f"Expected simple type, got {current_token}")

def procedure_declaration_part():
    while current_token and current_token[0] == "procedure":
        procedure_declaration()
        match("Special Token", ";")

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
    statement()
    while current_token and current_token[0] != "end":
        statement()
    match("Reserved Token", "end")

def statement():
    if current_token[0] in ["begin", "if", "while"]:
        structured_statement()
    else:
        simple_statement()
        match("Special Token", ";")

def simple_statement():
    if current_token[1] == "Identifier Token":
        if tokens[token_index + 1][0] == ":=":
            assignment_statement()
        else:
            procedure_statement()
    elif current_token[0] == "read":
        read_statement()
    elif current_token[0] == "write":
        write_statement()
    else:
        raise SyntaxError(f"Invalid simple statement: {current_token}")

def assignment_statement():
    variable()
    match("Assignment Token", ":=")
    expression()

def procedure_statement():
    procedure_identifier()

def procedure_identifier():
    match("Identifier Token")

def read_statement():
    match("Reserved Token", "read")
    match("Special Token", "(")
    input_variable()
    match("Special Token", ")")

def input_variable():
    variable()

def write_statement():
    match("Reserved Token", "write")
    match("Special Token", "(")
    output_value()
    match("Special Token", ")")

def output_value():
    expression()

def structured_statement():
    if current_token[0] == "begin":
        compound_statement()
    elif current_token[0] == "if":
        if_statement()
    elif current_token[0] == "while":
        while_statement()
    else:
        raise SyntaxError(f"Invalid structured statement: {current_token}")

def if_statement():
    match("Reserved Token", "if")
    expression()
    match("Reserved Token", "then")
    statement()
    if current_token and current_token[0] == "else":
        match("Reserved Token", "else")
        statement()

def while_statement():
    match("Reserved Token", "while")
    expression()
    match("Reserved Token", "do")
    statement()

def expression():
    simple_expression()
    if current_token and current_token[1] == "Relation Token":
        relational_operator_fun()
        simple_expression()

def simple_expression():
    term()
    while current_token and current_token[1] == "Addition Token":
        adding_operator_fun()
        term()

def term():
    factor()
    while current_token and current_token[1] == "Multiplication Token":
        multiplying_operator_fun()
        factor()

def factor():
    if current_token[1] == "Identifier Token":
        variable()
    elif current_token[1] == "Integer Token" or current_token[0] in ["true", "false"]:
        constant()
    elif current_token[0] == "(":
        match("Special Token", "(")
        expression()
        match("Special Token", ")")
    elif current_token[0] == "not":
        match("Reserved Token", "not")
        factor()
    else:
        raise SyntaxError(f"Invalid factor: {current_token}")

def relational_operator_fun():
    match("Relation Token")

def adding_operator_fun():
    match("Addition Token")

def multiplying_operator_fun():
    match("Multiplication Token")

def variable():
    match("Identifier Token")

def constant():
     if current_token[1] == "Integer Token":
        match("Integer Token")
     elif current_token[0] in ["true", "false"]:
        match("Data Type Token")
     else:
        raise SyntaxError(f"Invalid constant: {current_token}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <input_file>")
        sys.exit(1)

    try:
        parse(sys.argv[1])
        print("Parsing completed successfully.")
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()