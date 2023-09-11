import sys

if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../'])

from polyfill import is_numeric, create_varied_sequence
from ti_traits import TraitsReport
from dummy_types import *

_comma_inclusive_variations = create_varied_sequence('],', '[', max=10)
_comma_exclusive_variations = create_varied_sequence(']', '[', max=10)


def _flatten(lst):
    """Flatten a list of lists using for loop"""
    if not isinstance(lst, list):
        return [lst]
    if len(lst) == 0:
        return lst

    """Flatten an arbitrarily nested list using an iterative approach."""
    while any(isinstance(i, list) for i in lst):
        new_lst = []
        for i in lst:
            if isinstance(i, list):
                new_lst.extend(i)
            else:
                new_lst.append(i)
        lst = new_lst
    return lst


def _convert_element(x):
    if not isinstance(x, str):
        x = str(x).strip()
        if "−" in x:
            x.replace("−", "-")
    if is_numeric(x):
        try:
            return int(x) if int(x) == float(x) else float(x)
        except ValueError:
            pass
    else:
        return x.strip('"\'')


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
    if "'" in string:
        string = string.replace("'", "")
    if '"' in string:
        string = string.replace('"', '')
    return string


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


def _mat_to_mat(mat, rows: int, cols: int, fill: int = 0):
    if len(mat) > 0:
        if not isinstance(mat[0], list):
            mat = [mat]
    # Flatten the original matrix into a single list
    flat_list = [item for sublist in mat for item in sublist]

    # Create the new matrix with the reshaped dimensions, filling in values from the flattened list
    # and using the specified fill value for any extra spaces
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


def _remove_internal_brackets(x):
    return x.replace('][', ',').replace('],[', ',')


def _convert_to_ti_brackets(x):
    return x.replace('],[', '][').replace('], [', '][')


def _convert_to_py_brackets(x):
    return x.replace('][', '],[')


def _make_common_type(x):
    if not isinstance(x, str):
        x = str(x).strip()
    str_strip = _strip_lead_trail_brackets(x)
    str_norm = str_strip.replace(' ', '')
    return str_norm


def to_ti_mat(x):
    try:
        str_comm = _make_common_type(x)
        str_cnvbr = _convert_to_ti_brackets(str_comm)
        str_strip = _strip_quotes(str_cnvbr)
        return '[[' + str_strip + ']]'
    except Exception as e:
        print("There was an error converting to Py List\n{}".format(e))
        raise e


def to_py_list(x):
    try:
        str_comm = _make_common_type(x)
        str_rmbr = _remove_internal_brackets(str_comm)
        str_strip = _strip_quotes(str_rmbr)
        elements = str_strip.split(',')
        return [_convert_element(elem.strip()) for elem in elements]
    except Exception as e:
        print("There was an error converting to Py List\n{}".format(e))
        raise e


def to_py_mat(x):
    try:
        str_comm = _make_common_type(x)
        str_rmbr = _convert_to_py_brackets(str_comm)
        str_srrip = _strip_quotes(str_rmbr)
        elements = str_srrip.split('],[')
        return [[_convert_element(elem.strip()) for elem in row.split(',')] for row in elements]
    except Exception as e:
        print("There was an error converting to Py Mat\n{}".format(e))
        raise e


def to_ti_list(x):
    try:
        str_comm = _make_common_type(x)
        str_rmbr = _remove_internal_brackets(str_comm)
        str_strip = _strip_quotes(str_rmbr)
        return '{' + str_strip + '}'
    except Exception as e:
        print("There was an error converting to TI List\n{}".format(e))
        raise e
