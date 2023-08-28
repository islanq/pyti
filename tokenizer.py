import re

class MatrixParser:
    def __init__(self):
        # Compile patterns for faster searches
        self.num_pattern = re.compile(r'^\d+')
        self.var_pattern = re.compile(r'^[a-zA-Z_]\w*')
        self.op_pattern = re.compile(r'^[+*-]')

    def _get_next_token(self, s):
        # Check for a number at the start of the string
        match = self.num_pattern.match(s)
        if match:
            return match.group(0), len(match.group(0))
        
        # Check for a variable at the start of the string
        match = self.var_pattern.match(s)
        if match:
            return match.group(0), len(match.group(0))

        # Check for an operator at the start of the string
        match = self.op_pattern.match(s)
        if match:
            return match.group(0), len(match.group(0))

        return None, 0

    def tokenize_expression(self, expr):
        tokens = []
        i = 0
        while i < len(expr):
            token, length = self._get_next_token(expr[i:])
            if token:
                tokens.append(token)
                i += length
            else:
                i += 1
        return tokens

    def process_tokens(self, tokens):
        processed = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if self.num_pattern.match(token):
                processed.append(int(token))
            elif self.var_pattern.match(token):
                processed.append(token)
            elif token in ['+', '-', '*', '/']:
                prev = processed.pop() if processed else None
                i += 1
                next_token = tokens[i]
                processed.append("{}{}{}".format(prev, token, next_token))
            else:
                raise ValueError("Unsupported token: {}".format(token))
            i += 1
        return processed

    def parse_matrix(self, matrix_str):
        rows = matrix_str.strip().split("\n")
        matrix = []
        for row in rows:
            elements = row.strip().split(',')
            parsed_elements = []
            for element in elements:
                tokens = self.tokenize_expression(element)
                processed_expr = self.process_tokens(tokens)
                parsed_elements.extend(processed_expr)
            matrix.append(parsed_elements)
        return matrix
    
    
    
'''
parser = MatrixParser()
matrix_str = """
b+a, 2, a+3
3ax, c*2, 4
d-2, 5/e, e*3
"""

parsed_matrix = parser.parse_matrix(matrix_str)
for row in parsed_matrix:
    print(row)
'''