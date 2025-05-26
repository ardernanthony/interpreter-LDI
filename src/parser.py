from tokens import *
from environment import set_variable, get_variable

#The parser handles interpreting the structure of expressions and statements.
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[self.pos]  

    #moves to the next token if the current matches the expected type
    def eat(self, token_type):
        if self.current.type == token_type:
            self.pos += 1
            self.current = self.tokens[self.pos]
        else:
            raise Exception(f'Expected {token_type}, got {self.current.type}')

    #handles numbers, strings, booleans, variable names, negative values, NOT, and parenthesis
    def factor(self):
        token = self.current
        if token.type == NUMBER:
            self.eat(NUMBER)
            return token.value
        elif token.type == STRING:
            self.eat(STRING)
            return token.value
        elif token.type == BOOL:
            self.eat(BOOL)
            return token.value
        elif token.type == IDENTIFIER:
            name = token.value
            self.eat(IDENTIFIER)
            return get_variable(name)
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

    #handles addition and subtraction, and also supports string concatenation
    def arith_expr(self):
        result = self.term()
        while self.current.type in (PLUS, MINUS):
            if self.current.type == PLUS:
                self.eat(PLUS)
                right = self.term()
                if isinstance(result, str) and isinstance(right, str):
                    result = result + right
                elif isinstance(result, (int, float)) and isinstance(right, (int, float)):
                    result = result + right
                else:
                    raise Exception("TypeError: '+' must be number+number or string+string")
            elif self.current.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

    #handles comparison operations 
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

    #handles boolean logic operations 
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

    #full expression evaluation
    def expr(self):
        return self.logic()

    #parses and executes a full program
    def parse(self):
        while self.current.type != EOF:
            self.statement()

    #handles variable assignment and print statements
    def statement(self):
        if self.current.type == IDENTIFIER:
            var_name = self.current.value
            self.eat(IDENTIFIER)
            self.eat(ASSIGN)
            value = self.expr()
            set_variable(var_name, value)
        elif self.current.type == PRINT:
            self.eat(PRINT)
            value = self.expr()
            print(value)
        else:
            raise Exception(f"Unexpected statement start: {self.current}")
