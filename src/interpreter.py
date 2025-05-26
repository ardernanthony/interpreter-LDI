import sys
from lexer import tokenize
from parser import Parser

# main function

def main():
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <source-file>")
        return

    with open(sys.argv[1], 'r') as f:
        code = f.read()
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser.parse()

if __name__ == "__main__":
    main()
