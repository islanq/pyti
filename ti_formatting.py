from character_scripting import *
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

    # is_half = lambda x:

    if not is_matrix(mat):
        return ""
    rows = len(mat)
    cols = len(mat[0])

    mat_copy = [row.copy() for row in mat]

    # if sys.platform == 'win32':
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
    return result


def vanity_matrix(matrix, first_char='',
                  second_char='',
                  *,
                  row_sub_static='',
                  col_sub_static='',
                  row_sub_dynamic=False,
                  col_sub_dynamic=False):
    rows, cols = len(matrix), len(matrix[0])

    chr_counter = 97  # ASCII code for 'a'
    def subscript(x): return char_to_subscript(str(x))

    if row_sub_static:
        row_sub_static = subscript(row_sub_static)

    if col_sub_static:
        col_sub_static = subscript(col_sub_static)

    new_matrix = []
    for i in range(len(matrix)):

        row_sub_dynamic = subscript(i+1) if row_sub_dynamic else ''
        row_replacement = []

        for j in range(len(matrix[i])):

            char_first = chr(chr_counter) if first_char == '' else first_char
            char_second = second_char if second_char else ''

            # dynamic row subscript is set above in first loop
            row_subscript = row_sub_static if row_sub_static else ''

            # static column will override dynamic column subscript
            col_subscript = subscript(j+1) if col_sub_dynamic else ''
            col_subscript = col_sub_static if row_sub_static else ''

            txt_replacement = char_first + char_second + row_subscript + col_subscript

            row_replacement.append(txt_replacement)
            chr_counter += 1

        new_matrix.append(row_replacement)

    return new_matrix


def lower_triangular(matrix):
    """
    Set all elements above the main diagonal to zero.

    Parameters:
    matrix (list of list of int/float): The input matrix

    Returns:
    list of list of int/float: The lower triangular matrix
    """
    rows = len(matrix)
    for i in range(rows):
        for j in range(i + 1, rows):
            matrix[i][j] = 0
    return matrix


def upper_triangular(matrix):
    """
    Set all elements below the main diagonal to zero.

    Parameters:
    matrix (list of list of int/float): The input matrix

    Returns:
    list of list of int/float: The upper triangular matrix
    """

    rows = len(matrix)
    for i in range(1, rows):
        for j in range(i):
            matrix[i][j] = 0
    return matrix


def make_blank_matrix(rows, cols):
    """
    Create a blank matrix with all elements equal to zero.

    Parameters:
    rows (int): The number of rows
    cols (int): The number of columns

    Returns:
    list of list of int/float: The blank matrix
    """
    return [[0 for _ in range(cols)] for _ in range(rows)]
