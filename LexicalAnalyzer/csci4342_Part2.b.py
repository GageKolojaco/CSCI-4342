'''
	Gage Kolojaco CSCI4342 09/30/24
	Interpreter Pt. 2
 	Parser & Lexical Analyzer
'''

import sys
import re
from pathlib import Path #using to debug, TODO: remove later

#LEXICAL GRAMMAR
#letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] - replaced with regex
#digit - [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] - replaced with .isdigit
special_keyword = ['not', 'if', 'then', 'else', 'of', 'while', 'do', 'begin', 'end', 'read', 'write', 'var', 'array', 'procedure', 'program'] #i split this into special keyword and special char to better fit the "reserved" and "special" token types
special_char = ['|', '.', ',', ';', ':', '..', '(', ')']
assignment_operator = ':='
relational_operator =  ['=', '<>', '<', '<=', '>=', '>']
adding_operator = ['+', '-', 'or']
multiplying_operator = ['*', 'div', 'and']
predefined_identifier = ['integer', 'boolean', 'true', 'false']
token_pairs = []
token_index = 0
cur_token_pair = None

def main():
    #if len(sys.argv) != 2: #diabled for debugging.
        #print("Usage: python script_name.py <input_file>")
        #sys.exit(1)
    file_path = Path("c:/Users/Gagek/source/repos/CSCI4342-Gage-Kolojaco-HW/CSCI-4342/LexicalAnalyzer/input.txt")
    try:
        with file_path.open("r") as filehandle:
            parse(filehandle) #get file handle and open the file that is named in command line
        print("Parsing completed successfully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

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
        #this matches the rule  <identifier> -> <letter> { <letter or digit> }
        return "Identifier Token"
    elif token in special_char:
        return "Special Token"
    else:
        return "Invalid Token"

def parse(filehandle):
    token_regex = re.compile(r'(\w+|\:=|<=|>=|<>|[^\w\s])')  # token regex pattern


    for line in filehandle:   # iterate through each line
        line = line.strip()   # strip whitespace
        line_tokens = token_regex.findall(line)  # find tokens in line

        for token in line_tokens:  # iterate through tokens
            token_type = tokenator(token)  # get token type from tokenator function
            token_pairs.append((token_type, token))  # add token and token type as a tuple.
            print(f"{token_type} : {token}")  # print token and type if needed
    
    global cur_token_pair, token_index
    
    cur_token_pair = token_pairs[0] if token_pairs else None
    
    program()

def advance():
    global token_pairs, token_index, cur_token_pair
    token_index += 1
    if token_index < len(token_pairs):
        cur_token_pair = token_pairs[token_index]
    else:
        cur_token_pair = None
        
def match(expected_type, expected_val=None):
    global cur_token_pair
    if not cur_token_pair:
        raise SyntaxError(f"Expected {expected_type}, got end of input")
    if cur_token_pair[0] != expected_type and cur_token_pair[0] not in [
        "Addition Token",
        "Multiplication Token",
        "Relation Token",
        "Integer Token",
        "Data Type Token"
    ]:
        raise SyntaxError(f"Expected {expected_type}, got {cur_token_pair[1]}")
    if expected_val is not None and cur_token_pair[1] != expected_val:
        raise SyntaxError(f"Expected '{expected_val}', got '{cur_token_pair[0]}'")
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
    global cur_token_pair
    if cur_token_pair and cur_token_pair[1] == "var":
        match("Reserved Token", "var")
        variable_declaration()
        match("Special Token", ";")
        while cur_token_pair and cur_token_pair[0] == "Identifier Token":
            variable_declaration()
            match("Special Token", ";")

def variable_declaration():
    global cur_token_pair
    match("Identifier Token")
    while cur_token_pair and cur_token_pair[1] == ",":
        match("Special Token", ",")
        match("Identifier Token")
    match("Special Token", ":")
    simple_type()

def simple_type():
    global cur_token_pair
    if cur_token_pair[1] in ["integer", "boolean"]:
        match("Data Type Token")
    else:
        raise SyntaxError(f"Expected simple type, got {cur_token_pair}")

def procedure_declaration_part():
    global cur_token_pair
    while cur_token_pair and cur_token_pair[1] == "procedure":
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
    global cur_token_pair
    match("Reserved Token", "begin")
    statement()
    while cur_token_pair and cur_token_pair[1] != "end":
        statement()
    match("Reserved Token", "end")

def statement():
    global cur_token_pair
    if cur_token_pair[1] in ["begin", "if", "while"]:
        structured_statement()
    else:
        simple_statement()
        match("Special Token", ";")

def simple_statement():
    global cur_token_pair, token_index
    if cur_token_pair[0] == "Identifier Token":
        if token_pairs[token_index + 1][1] == ":=":
            assignment_statement()
        else:
            procedure_statement()
    elif cur_token_pair[1] == "read":
        read_statement()
    elif cur_token_pair[1] == "write":
        write_statement()
    else:
        raise SyntaxError(f"Invalid simple statement: {cur_token_pair}")

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
    global cur_token_pair
    if cur_token_pair[1] == "begin":
        compound_statement()
    elif cur_token_pair[1] == "if":
        if_statement()
    elif cur_token_pair[1] == "while":
        while_statement()
    else:
        raise SyntaxError(f"Invalid structured statement: {cur_token_pair}")

def if_statement():
    global cur_token_pair
    match("Reserved Token", "if")
    expression()
    match("Reserved Token", "then")
    statement()
    if cur_token_pair and cur_token_pair[1] == "else":
        match("Reserved Token", "else")
        statement()

def while_statement():
    match("Reserved Token", "while")
    expression()
    match("Reserved Token", "do")
    statement()

def expression():
    global cur_token_pair
    simple_expression()
    if cur_token_pair and cur_token_pair[0] == "Relation Token":
        relational_operator_fun()
        simple_expression()

def simple_expression():
    global cur_token_pair
    term()
    while cur_token_pair and cur_token_pair[0] == "Addition Token":
        adding_operator_fun()
        term()

def term():
    global cur_token_pair
    factor()
    while cur_token_pair and cur_token_pair[0] == "Multiplication Token":
        multiplying_operator_fun()
        factor()

def factor():
    global cur_token_pair
    if cur_token_pair[0] == "Identifier Token":
        variable()
    elif cur_token_pair[0] == "Integer Token" or cur_token_pair[0] in ["true", "false"]:
        constant()
    elif cur_token_pair[1] == "(":
        match("Special Token", "(")
        expression()
        match("Special Token", ")")
    elif cur_token_pair[1] == "not":
        match("Reserved Token", "not")
        factor()
    else:
        raise SyntaxError(f"Invalid factor: {cur_token_pair}")

def relational_operator_fun():
    match("Relation Token")

def adding_operator_fun():
    match("Addition Token")

def multiplying_operator_fun():
    match("Multiplication Token")

def variable():
    match("Identifier Token")

def constant():
    global cur_token_pair
    if cur_token_pair[0] == "Integer Token":
        match("Integer Token")
    elif cur_token_pair[1] in ["true", "false"]:
        match("Data Type Token")
    else:
        raise SyntaxError(f"Invalid constant: {cur_token_pair}")

if __name__ == '__main__':
    main()
    
