is_digit = lambda s: all(48 <= ord(c) <= 57 for c in s)
is_numeric = lambda s: all(48 <= ord(c) <= 57 or ord(c) == 46 for c in s)
is_alpha = lambda s: all(65 <= ord(c) <= 90 or 97 <= ord(c) <= 122 for c in s)
is_alnum = lambda s: is_alpha(s) or is_digit(s) or is_numeric(s)
import re

def tokenize(expr):
    tokens = []
    current_token = ''
    for c in expr:
        if c in ' +-*/^()':
            if current_token:
                tokens.append(current_token)
                current_token = ''
            if c != ' ':
                tokens.append(c)
        else:
            current_token += c
    if current_token:
        tokens.append(current_token)
    return tokens

# removing named variables
def parse_tokens(infix_tokens, known_variables=None):
    # Shunting Yard algorithm with unary operators
    output_queue = []
    operator_stack = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'u-': 4}  # Add precedence for unary minus ('u-')
    right_associative = {'^'}
    
    can_be_unary = True  # Flag to check if the next operator can be unary

    for token in infix_tokens:
        if is_digit(token) or is_numeric(token) or (known_variables is not None and token in known_variables) or is_alpha(token) or '_' in token:
            output_queue.append(token)
            can_be_unary = False  # Reset the flag
        elif token in "+-*/^":
            if can_be_unary and token == '-':  # Handle unary minus
                operator_stack.append('u-')  # Use a different symbol to distinguish unary minus
            else:
                while (operator_stack and 
                       (precedence.get(token, 0) < precedence.get(operator_stack[-1], 0) or 
                       (token not in right_associative and precedence.get(token, 0) == precedence.get(operator_stack[-1], 0)))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            can_be_unary = False  # Reset the flag
        elif token == "(":
            operator_stack.append(token)
            can_be_unary = True  # Set the flag if an opening parenthesis is encountered
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            operator_stack.pop()
            can_be_unary = False  # Reset the flag

        if token in "+-*/^(":
            can_be_unary = True  # Set the flag if an operator or opening parenthesis is encountered
            
    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue

def evaluate(postfix_tokens, known_variables=None):
    
    stack = []

    try:
        for i, token in enumerate(postfix_tokens):
            if is_numeric(token) or (is_digit(token.replace('.', '', 1))):
                stack.append(token)
            elif known_variables and token in known_variables:
                stack.append(token)
            elif token in "+-*/^":
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '+':
                    stack.append("({} + {})".format(operand1, operand2))
                elif token == '-':
                    stack.append("({} - {})".format(operand1, operand2))
                elif token == '*':
                    stack.append("({} * {})".format(operand1, operand2))
                elif token == '/':
                    stack.append("({} / {})".format(operand1, operand2))
                elif token == '^':
                    stack.append("({} ^ {})".format(operand1, operand2))
            elif token == 'u-':  # Handling unary minus
                operand = stack.pop()
                stack.append("(-{})".format(operand))
            else:  # Assume it's a variable if not recognized
                stack.append(token)
        
        return stack[0]

    except IndexError:
        print("Error: Stack underflow. Check if the postfix expression is correct.")
        print("Current stack:", stack)
        print("Postfix expression:", postfix_tokens)
        return None

def format_expression(expr, named_vars=None):
    expr, formatted_expr, current_var = ' '.join(expr.split()), '', ''
    in_numeric_token = False
    last_token_was_alpha = False

    if expr.count('(') != expr.count(')'):
        raise Exception("Error: Unbalanced parentheses.")

    def append_current_var():
        nonlocal formatted_expr, current_var, in_numeric_token, last_token_was_alpha
        if current_var:
            if is_numeric(current_var[0]) and any(is_alpha(c) or c == '_' for c in current_var[1:]):
                formatted_expr += current_var[0] + ' * ' + current_var[1:] + ' '
            elif '_' in current_var:
                formatted_expr += current_var + ' '
            elif named_vars and current_var in named_vars:
                formatted_expr += current_var + ' '
            elif in_numeric_token:
                formatted_expr += current_var + ' '
            else:
                formatted_expr += ' * '.join(list(current_var)) + ' '
            
            last_token_was_alpha = is_alpha(current_var[-1])
            current_var = ''
            in_numeric_token = False

    for c in expr:
        if is_alnum(c) or c == '_':
            if last_token_was_alpha and is_numeric(c):
                append_current_var()  # Handle edge cases like "19+aa" becoming "19 + aa"
            current_var += c
            if is_numeric(c):
                in_numeric_token = True
            else:
                in_numeric_token = False
            continue

        if c == '.' and in_numeric_token:
            current_var += c
            continue

        append_current_var()
        formatted_expr += c + ' '

    append_current_var()
    return ' '.join(formatted_expr.split()).strip()

