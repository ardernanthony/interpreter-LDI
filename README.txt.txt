README - Stage 4 Language Interpreter

This project is a simple interpreter written in Python that parses and executes a custom scripting language. It supports arithmetic, booleans, strings, global variables, and print statements.

---

FEATURES SUPPORTED:

1. Arithmetic
- addition, subtraction, multiplication, division
- operator precedence
- brackets
Example:
    1 + 2 * 3         # result: 7
    (1 + 2) * 3       # result: 9

2. Booleans
- true / false values
- comparison operators: ==, !=, <, <=, >, >=
- logical operators: and, or, not
Example:
    true and false    # result: false
    5 > 3             # result: true

3. Strings
- string literals in quotes
- string + string concatenation
- string comparison using == and !=
Example:
    "hello" + " world"   # result: "hello world"
    "a" == "b"           # result: false

4. Global Variables
- assignment and reuse across lines
- supports numeric and string values
Example:
    x = 5
    x = x + 2
    print x             # result: 7

5. Type Safety
- type mismatch raises errors (e.g., string + number)
Example:
    x = "dog" + 5       # error

6. Printing
- using `print` followed by an expression
Example:
    print 1 + 2         # output: 3
    print "hi"          # output: hi

7. Comments
- any line starting with `#` is ignored

---

PROJECT STRUCTURE:

src/
── interpreter.py     # entry point
── lexer.py           # turns input into tokens
── parser.py          # parses and evaluates the program
── tokens.py          # defines token types
── environment.py     # stores global variables

examples/
  - calc.txt
  - floatTest.txt
  - logic.txt
  - text.txt
  - vars.txt

---

HOW TO RUN:

1. Open a terminal
2. Navigate to the project directory
3. Run:

    python src/interpreter.py examples/vars.txt

You can swap out the example file for any other.

---

NOT SUPPORTED:
- interactive mode
- lists
- user input
- functions
- test framework
