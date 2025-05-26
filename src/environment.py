#handles variable storage
# dictionary to store variable names and values
variables = {}

#stores a value into a variable name
def set_variable(name, value):
    variables[name] = value

#retrieves a variable's value, or throws an error if undefined
def get_variable(name):
    if name not in variables:
        raise Exception(f"Variable '{name}' is not defined")
    return variables[name]
