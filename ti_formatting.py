import sys

if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../'])

from frac import Frac
def most_accurate(elem):
        frac = Frac(elem)
        if frac.denominator == 2:
            return frac
        if len(str(frac)) <= len(str(elem)):
            return frac
        return elem

def display_matrices(matrices):
    """Display a list of matrices side by side in a formatted way with .format method."""

    # Get the maximum width of each column in each matrix
    col_widths = [
        [max(len(str(row[i])) for row in matrix)
         for i in range(len(matrix[0]))]
        for matrix in matrices
    ]

    # Create a formatted string for each row
    rows = []

    # Get the number of rows in each matrix
    num_rows = [len(matrix) for matrix in matrices]

    # Get the maximum number of rows across all matrices
    max_rows = max(num_rows)

    for idx in range(max_rows):
        row_strs = []
        for m, matrix in enumerate(matrices):
            if idx < num_rows[m]:
                row = matrix[idx]
                row_str = (
                    "⎡" + "  ".join("{:>{}}".format(str(row[i]), col_widths[m][i]) for i in range(len(row))) + "⎤" if idx == 0
                    else "⎢" + "  ".join("{:>{}}".format(str(row[i]), col_widths[m][i]) for i in range(len(row))) + "⎥" if idx != num_rows[m] - 1
                    else "⎣" + "  ".join("{:>{}}".format(str(row[i]), col_widths[m][i]) for i in range(len(row))) + "⎦"
                )
            else:
                row_str = " " * \
                    (sum(col_widths[m]) + len(col_widths[m]) * 2 - 1)

            row_strs.append(row_str)

        # Join the formatted strings for the current row from all matrices
        rows.append(" ".join(row_strs))

    # Join the rows with newline characters to get the final string
    matrix_str = "\n".join(rows)

    return matrix_str

# def display_matrix(matrix):
#     """Display a matrix in a formatted way with .format method."""
    
#     # Get the maximum width of each column
#     col_widths = [
#         max(len(str(row[i])) for row in matrix) for i in range(len(matrix[0]))
#     ]
  
#     # Create a formatted string for each row
#     rows = [
#         "⎡" + "  ".join("{:>{}}".format(str(row[i]), col_widths[i]) for i in range(len(row))) + "⎤" if idx == 0
#         else "⎢" + "  ".join("{:>{}}".format(str(row[i]), col_widths[i]) for i in range(len(row))) + "⎥" if idx != len(matrix) - 1
#         else "⎣" + "  ".join("{:>{}}".format(str(row[i]), col_widths[i]) for i in range(len(row))) + "⎦"
#         for idx, row in enumerate(matrix)
#     ]
    
#     # Join the rows with newline characters to get the final string
#     matrix_str = "\n".join(rows)
    
#     return matrix_str

def display_matrix(matrix):
    """Display a matrix in a formatted way with .format method."""
    
    # Get the maximum width of each column
    col_widths = [
        max(len(str(row[i])) for row in matrix) for i in range(len(matrix[0]))
    ]
  
    # Create a formatted string for each row
    rows = [
        "|" + "  ".join("{:>{}}".format(str(row[i]), col_widths[i]) for i in range(len(row))) + "|" if idx == 0
        else "|" + "  ".join("{:>{}}".format(str(row[i]), col_widths[i]) for i in range(len(row))) + "|" if idx != len(matrix) - 1
        else "|" + "  ".join("{:>{}}".format(str(row[i]), col_widths[i]) for i in range(len(row))) + "|"
        for idx, row in enumerate(matrix)
    ]
    
    # Join the rows with newline characters to get the final string
    matrix_str = "\n".join(rows)
    
    return matrix_str
  
def mat_repr(mat):
    from matrix_tools import is_matrix
    from frac import Frac
    
    

        
        
    #is_half = lambda x: 
    
    if not is_matrix(mat):
        return ""
    rows = len(mat)
    cols = len(mat[0])
    
    mat_copy = [row.copy() for row in mat]
    
    #if sys.platform == 'win32':
    # Step 2: Convert float elements to fraction if fraction representation is shorter
    for i in range(rows):
        for j in range(cols):
            elem = mat_copy[i][j]
            if isinstance(elem, float):
                mat_copy[i][j] = most_accurate(elem)
        
    # Step 3: Find the maximum length for each column
    str_lst = [[str(ele) for ele in row] for row in mat_copy]
    max_lens = [max(map(len, col)) for col in zip(*str_lst)]
    
    # Step 4: Build the output string using the max length for each column
    rows_strs = [
        '[' + ' '.join("{:>{}}".format(str(ele), max_lens[i])
            for i, ele in enumerate(row)) + ']'
                for row in str_lst
    ]
    result = '\n'.join(rows_strs).strip().replace('"', '').replace("'", '')
    return  result 
