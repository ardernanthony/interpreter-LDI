import re
import sys

#below are the types of symbols our parser understands.
NUMBER = 'NUMBER'
BOOL = 'BOOL'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EQ = 'EQ'     
NEQ = 'NEQ'  
LT = 'LT'     
GT = 'GT'     
LE = 'LE'     
GE = 'GE'     
AND = 'AND'   
OR = 'OR'     
NOT = 'NOT'   
EOF = 'EOF'  

# Each token is given a type and a value.
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'{self.type}:{self.value}'



# This function turns a string into tokens.
def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isspace():
            i += 1  
        elif text[i].isdigit() or text[i] == '.':
            # Build a number token (supporting decimals)
            num = ''
            while i < len(text) and (text[i].isdigit() or text[i] == '.'):
                num += text[i]
                i += 1
            tokens.append(Token(NUMBER, float(num)))
        elif text[i:i+4] == 'true':
            tokens.append(Token(BOOL, True))
            i += 4
        elif text[i:i+5] == 'false':
            tokens.append(Token(BOOL, False))
            i += 5
        elif text[i:i+3] == 'and':
            tokens.append(Token(AND, 'and'))
            i += 3
        elif text[i:i+2] == 'or':
            tokens.append(Token(OR, 'or'))
            i += 2
        elif text[i] == '!':
            if i+1 < len(text) and text[i+1] == '=':
                tokens.append(Token(NEQ, '!='))
                i += 2
            else:
                tokens.append(Token(NOT, '!'))
                i += 1
        elif text[i] == '=' and i+1 < len(text) and text[i+1] == '=':
            tokens.append(Token(EQ, '=='))
            i += 2
        elif text[i] == '<':
            if i+1 < len(text) and text[i+1] == '=':
                tokens.append(Token(LE, '<='))
                i += 2
            else:
                tokens.append(Token(LT, '<'))
                i += 1
        elif text[i] == '>':
            if i+1 < len(text) and text[i+1] == '=':
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


#This uses recursive functions to parse and evaluate expressions.
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[self.pos]  # Starts at the first token

    def eat(self, token_type):
        if self.current.type == token_type:
            self.pos += 1
            self.current = self.tokens[self.pos]
        else:
            raise Exception(f'Expected {token_type}, got {self.current.type}')

    #handles numbers, negative numbers, boolean values, NOT, and parenthesis
    def factor(self):
        token = self.current
        if token.type == NUMBER:
            self.eat(NUMBER)
            return token.value
        elif token.type == BOOL:
            self.eat(BOOL)
            return token.value
        elif token.type == MINUS:
            self.eat(MINUS)
            return -self.factor()
        elif token.type == NOT:
            self.eat(NOT)
            return not self.factor()
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        else:
            raise Exception(f'Unexpected token in factor: {token.type}')

    #handles multiplication and division
    def term(self):
        result = self.factor()
        while self.current.type in (MUL, DIV):
            if self.current.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif self.current.type == DIV:
                self.eat(DIV)
                result /= self.factor()
        return result

    #handles addition and subtraction
    def arith_expr(self):
        result = self.term()
        while self.current.type in (PLUS, MINUS):
            if self.current.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif self.current.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

    #handles comparison operators
    def comparison(self):
        result = self.arith_expr()
        while self.current.type in (EQ, NEQ, LT, GT, LE, GE):
            if self.current.type == EQ:
                self.eat(EQ)
                result = result == self.arith_expr()
            elif self.current.type == NEQ:
                self.eat(NEQ)
                result = result != self.arith_expr()
            elif self.current.type == LT:
                self.eat(LT)
                result = result < self.arith_expr()
            elif self.current.type == GT:
                self.eat(GT)
                result = result > self.arith_expr()
            elif self.current.type == LE:
                self.eat(LE)
                result = result <= self.arith_expr()
            elif self.current.type == GE:
                self.eat(GE)
                result = result >= self.arith_expr()
        return result

    #handles boolean logic operators (and, or)
    def logic(self):
        result = self.comparison()
        while self.current.type in (AND, OR):
            if self.current.type == AND:
                self.eat(AND)
                result = result and self.comparison()
            elif self.current.type == OR:
                self.eat(OR)
                result = result or self.comparison()
        return result

    #expression parser
    def expr(self):
        return self.logic()


# This runs the tokenizer and parser for a single line of input.
def evaluate_expression(expression):
    tokens = tokenize(expression)
    parser = Parser(tokens)
    return parser.expr()


#MAIN FUNCTION
#reads a file and evaluates each line.
def main():
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <input-file>")
        return

    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                try:
                    result = evaluate_expression(line)
                    print(f"{line} => {result}")
                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    main()
