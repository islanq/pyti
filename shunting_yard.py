# Tokenizing the infix expression for better parsing
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

# Shunting Yard algorithm
def parse_tokens(infix_tokens, known_variables=None):
    is_digit = lambda s: all(48 <= ord(c) <= 57 for c in s)
    is_numeric = lambda s: all(48 <= ord(c) <= 57 or ord(c) == 46 for c in s)
    is_alpha = lambda s: all(65 <= ord(c) <= 90 or 97 <= ord(c) <= 122 for c in s)
    
    output_queue = []
    operator_stack = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    right_associative = {'^'}

    for token in infix_tokens:
        if is_digit(token) or is_numeric(token) or (known_variables is not None and token in known_variables) or is_alpha(token):
            output_queue.append(token)
        elif token in "+-*/^":
            while (operator_stack and 
                   (precedence.get(token, 0) < precedence.get(operator_stack[-1], 0) or 
                   (token not in right_associative and precedence.get(token, 0) == precedence.get(operator_stack[-1], 0)))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            operator_stack.pop()
    while operator_stack:
        output_queue.append(operator_stack.pop())
    return output_queue

# Function to symbolically evaluate a postfix expression
def evaluate(postfix_tokens, known_variables=None):
    is_digit = lambda s: all(48 <= ord(c) <= 57 for c in s)
    is_numeric = lambda s: all(48 <= ord(c) <= 57 or ord(c) == 46 for c in s)
    is_alpha = lambda s: all(65 <= ord(c) <= 90 or 97 <= ord(c) <= 122 for c in s)
    stack = []
    try:
        for token in postfix_tokens:
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
            else:  # Assume it's a variable if not recognized
                stack.append(token)
        return stack[0]
    except IndexError:
        print("Error: Stack underflow. Check if the postfix expression is correct.")
        print("Current stack:", stack)
        print("Postfix expression:", postfix_tokens)
        return None

def format_expression(expr, named_vars=None):
    expr, formatted_expr, current_var, is_named_var = ' '.join(expr.split()), '', '', False

    for c in expr:
        if c.isalnum() or c == '_':  
            current_var += c
            is_named_var = (named_vars and current_var in named_vars) or current_var.startswith('_') or current_var.endswith('_')
            continue

        formatted_expr += current_var if is_named_var else ' * '.join(list(current_var))
        formatted_expr += ' ' + c + ' '
        current_var, is_named_var = '', False

    formatted_expr += current_var if is_named_var else ' * '.join(list(current_var))
    return ' '.join(formatted_expr.split()).strip()



fomatted = format_expression("(2a)+8d^2")
tokenized = tokenize(fomatted)
parsed = parse_tokens(tokenized)
evaluated = evaluate(parsed)
print(evaluated)


"""# Test the final code
#symbols("a b c d")
infix_expr = "( a + b ) * ( c + d^2 ) + 1.23"
tokenized_expr = tokenize(infix_expr)
postfix_expr = parse_tokens(tokenized_expr)
print("Infix expression:", infix_expr)
print("Tokenized expression:", tokenized_expr)
print("Postfix expression:", " ".join(postfix_expr))
print("Symbolic evaluation result:", evaluate(postfix_expr))"""



