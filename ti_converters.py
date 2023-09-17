
import sys
if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../', '.'])

from wrappers import debug_in_out
from polyfill import is_numeric, create_varied_sequence
from ti_traits import TraitsReport
from matrix_tools import flatten, convert_element
from dummy_types import *
from polyfill import map_replace

_comma_inclusive_variations = create_varied_sequence('],', '[', max=10)
_comma_exclusive_variations = create_varied_sequence(']', '[', max=10)


def _ensure_double_brackets(mat_str):
    mat_str = _strip_lead_trail_brackets(mat_str)
    return '[[' + mat_str + ']]'


def _ensure_single_brackets(string):
    string = _strip_lead_trail_brackets(string)
    return '[' + string + ']'


def _strip_lead_trail_brackets(string):
    while string.startswith('['):
        string = string.lstrip('[')
    while string.endswith(']'):
        string = string.rstrip(']')
    return string.replace('{', '').replace('}', '')


def _strip_quotes(string):
    replacements = {
        "'": '',
        '"': ''
    }
    return map_replace(string, replacements)


def _list_to_mat(lst, num_cols: int = 1, fill: (int, str) = 0):
    """_summary_

    Args:
        lst (_type_): _description_ python list
        num_cols (int, optional): _description_. Defaults to 1.
        fill (int, str, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_ python matrix (list of lists)
    """
    # Calculate the number of rows needed
    num_rows = (len(lst) + num_cols - 1) // num_cols

    # Create the matrix with the elements from the list and fill the remaining spaces with 0s
    mat = [[fill] * num_cols for _ in range(num_rows)]
    for i, val in enumerate(lst):
        row = i // num_cols
        col = i % num_cols
        mat[row][col] = val

    return mat


def _mat_to_mat(mat, elem_per_row: int, fill: int = 0):
    # Ensure mat is a list of lists
    if len(mat) > 0:
        if not isinstance(mat[0], list):
            mat = [mat]
    # Flatten the original matrix into a single list
    flat_list = flatten(mat)

    # Determine the number of rows and columns for the reshaped matrix
    rows = len(flat_list) // elem_per_row
    if len(flat_list) % elem_per_row != 0:
        rows += 1
    cols = elem_per_row

    # Create the new matrix with the reshaped dimensions,
    # filling in values from the flattened list and
    # using the specified fill value for any extra spaces
    new_mat = []
    for i in range(rows):
        row = []
        for j in range(cols):
            index = i * cols + j
            if index < len(flat_list):
                row.append(flat_list[index])
            else:
                row.append(fill)
        new_mat.append(row)

    return new_mat


def _remove_inner_brackets(x):
    return x.replace('][', ',').replace('],[', ',')


def _convert_to_ti_brackets(x):
    return x.replace('],[', '][').replace('], [', '][')


def _convert_to_py_brackets(x):
    return x.replace('][', '],[')


def _make_common_type(x):
    if not isinstance(x, str):
        x = str(x).strip()
    no_space = x.replace(' ', '')
    no_lines = no_space.replace(r'\n', '')
    return _strip_lead_trail_brackets(no_lines)

# Py Converters


@debug_in_out(enabled=False)
def to_py_mat(x, elemen_per_row: int = None, fill: int = 0) -> list:
    try:
        str_comm = _make_common_type(x)
        str_rmbr = _convert_to_py_brackets(str_comm)
        str_strip = _strip_quotes(str_rmbr)
        elements = str_strip.split('],[')
        py_matrix = [[convert_element(elem.strip())
                      for elem in row.split(',')] for row in elements]
        if elemen_per_row:
            py_matrix = _mat_to_mat(py_matrix, elemen_per_row)

        return py_matrix

    except Exception as e:
        print("There was an error converting to Py Mat\n{}".format(e))
        raise e


def to_py_list(x) -> list:
    try:
        str_comm = _make_common_type(x)
        str_rmbr = _remove_inner_brackets(str_comm)
        str_strip = _strip_quotes(str_rmbr)
        elements = str_strip.split(',')
        return [convert_element(elem.strip()) for elem in elements]
    except Exception as e:
        print("There was an error converting to Py List\n{}".format(e))
        raise e


def to_py_row_vec(x) -> list:
    py_list = flatten(to_py_list(x))
    return to_py_mat(py_list, len(py_list))


def to_py_col_vec(x):
    py_list = to_py_list(x)
    py_list = flatten(to_py_list(py_list))
    return [[elem] for elem in py_list]

# TI Converters


def to_ti_list(x) -> str:
    try:
        str_comm = _make_common_type(x)
        str_rmbr = _remove_inner_brackets(str_comm)
        str_strip = _strip_quotes(str_rmbr)
        return '{' + str_strip + '}'
    except Exception as e:
        print("There was an error converting to TI List\n{}".format(e))
        raise e


def to_ti_mat(x) -> str:
    try:
        str_comm = _make_common_type(x)
        str_cnvbr = _convert_to_ti_brackets(str_comm)
        str_strip = _strip_quotes(str_cnvbr)
        return '[[' + str_strip + ']]'
    except Exception as e:
        print("There was an error converting to Py List\n{}".format(e))
        raise e


def to_ti_col_vec(x) -> str:
    try:
        py_col_vec = to_py_col_vec(x)
        ti_col_vec = to_ti_mat(py_col_vec)
        return ti_col_vec
    except Exception as e:
        print("There was an error converting to TI Col Vec\n{}".format(e))
        raise e


def to_ti_row_vec(x) -> str:
    try:
        py_row_vec = to_py_row_vec(x)
        ti_row_vec = to_ti_mat(py_row_vec)
        return ti_row_vec
    except Exception as e:
        print("There was an error converting to TI Col Vec\n{}".format(e))
        raise e


def parse_list(input):
    input = str(input).strip().replace(',', '],[').replace(r'\n', '')
    return to_py_list(input)


def parse_matrix(input, col_vec=False):
    input = str(input).strip().replace(';', '],[')
    return to_py_col_vec(input) if col_vec else to_py_mat(input)


def append_vectors(matrix, column):
    if isinstance(column, list):
        column = flatten(column)
    if len(matrix) != len(column):
        raise ValueError(
            "Matrix and column must have the same number of rows.")

    result_matrix = [matrix_row + ([col_value[0]] if isinstance(
        col_value, list) else [col_value])
        for matrix_row, col_value in zip(matrix, column)]

    return result_matrix


def parse_matrix_iter(input_str):
    rows = input_str.split(';')
    matrix = []
    for row in rows:
        values = row.split(',')
        matrix_row = [int(val) for val in values]
        matrix.append(matrix_row)
    return matrix


def append_vectors(mat_or_column_vector, column_vector=None):
    if column_vector is None:
        column_vector = mat_or_column_vector
        mat_or_column_vector = [[] for _ in range(len(column_vector))]

    if len(mat_or_column_vector) == 0 or len(mat_or_column_vector) == len(column_vector):
        for i in range(len(mat_or_column_vector)):
            mat_or_column_vector[i].append(column_vector[i])
    else:
        raise ValueError(
            "All column vectors must have the same number of rows.")
    matrix = [flatten(x) for x in mat_or_column_vector]
    return matrix
