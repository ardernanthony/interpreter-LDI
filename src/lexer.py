from tokens import *

#Each token is given a type and a value.
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'{self.type}:{self.value}'


#This function turns a string into a list of tokens.
def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isspace():
            i += 1
        elif text[i] == '#':
            while i < len(text) and text[i] != '\n':
                i += 1
        elif text[i] == '"':
            # build a string token inside quotes
            i += 1
            value = ''
            while i < len(text) and text[i] != '"':
                value += text[i]
                i += 1
            if i >= len(text):
                raise Exception("Unclosed string literal")
            i += 1
            tokens.append(Token(STRING, value))
        elif text[i].isalpha():
            # read identifiers or keywords
            id_str = ''
            while i < len(text) and (text[i].isalnum() or text[i] == '_'):
                id_str += text[i]
                i += 1
            if id_str == 'true':
                tokens.append(Token(BOOL, True))
            elif id_str == 'false':
                tokens.append(Token(BOOL, False))
            elif id_str == 'print':
                tokens.append(Token(PRINT, 'print'))
            else:
                tokens.append(Token(IDENTIFIER, id_str))
        elif text[i].isdigit() or text[i] == '.':
            # build a number token (supporting decimals)
            num = ''
            while i < len(text) and (text[i].isdigit() or text[i] == '.'):
                num += text[i]
                i += 1
            tokens.append(Token(NUMBER, float(num)))
        elif text[i] == '=':
            if i + 1 < len(text) and text[i+1] == '=':
                tokens.append(Token(EQ, '=='))
                i += 2
            else:
                tokens.append(Token(ASSIGN, '='))
                i += 1
        elif text[i] == '!':
            if i + 1 < len(text) and text[i+1] == '=':
                tokens.append(Token(NEQ, '!='))
                i += 2
            else:
                tokens.append(Token(NOT, '!'))
                i += 1
        elif text[i] == '<':
            if i + 1 < len(text) and text[i+1] == '=':
                tokens.append(Token(LE, '<='))
                i += 2
            else:
                tokens.append(Token(LT, '<'))
                i += 1
        elif text[i] == '>':
            if i + 1 < len(text) and text[i+1] == '=':
                tokens.append(Token(GE, '>='))
                i += 2
            else:
                tokens.append(Token(GT, '>'))
                i += 1
        elif text[i] == '+':
            tokens.append(Token(PLUS, '+'))
            i += 1
        elif text[i] == '-':
            tokens.append(Token(MINUS, '-'))
            i += 1
        elif text[i] == '*':
            tokens.append(Token(MUL, '*'))
            i += 1
        elif text[i] == '/':
            tokens.append(Token(DIV, '/'))
            i += 1
        elif text[i] == '(':
            tokens.append(Token(LPAREN, '('))
            i += 1
        elif text[i] == ')':
            tokens.append(Token(RPAREN, ')'))
            i += 1
        else:
            raise Exception(f'Unexpected character: {text[i]}')

    tokens.append(Token(EOF, None))
    return tokens
