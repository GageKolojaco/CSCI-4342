import sys
import re

#LEXICAL GRAMMAR
letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
digit = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
special_keyword = ['|', '.', ',', ';', ':', '..', 'not', 'if', 'then', 'else', 'of', 'while', 'do', 'begin', 'end', 'read', 'write', 'var', 'array', 'procedure', 'program']
assignment_operator = ':='
relational_operator =  ['=', '<>', '<', '<=', '>=', '>']
adding_operator = ['+', '-', 'or']
multiplying_operator = ['*', 'div', 'and']
predefined_identifier = ['integer', 'boolean', 'true', 'false']

def main(): #TODO-Update function to match new functions
    parse(open(sys.argv[1])) #get file handle and open the file that is named in command line

def parse(filehandle):
	input = filehandle.readlines()
	

#defines each token appropriately
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
    elif token in digit:
        return "Integer Token"
    elif re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', token): 
        #this matches the rule  <identifier> -> <letter> { <letter or digit> }
        return "Identifier Token"
    elif token in ['(', ')', ',', ';', ':', '.']:
        return "Special Token"
    else:
        return "Invalid Token"

if __name__ == '__main__':
    main()
    
