import sys

if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../', '.'])

from polyfill import is_numeric as isnum
from wrappers import debug_in_out
from ti_formatting import most_accurate
from collections import namedtuple

Dimensions = namedtuple('Dimensions', ['rows', 'cols'])


def flatten(lst):
    """_summary_
    Flattens a list of lists into a single list
    example: `[[1, 2], [3, 4]]` -> `[1, 2, 3, 4]`
    Args:
        lst (_type_): _description_ list of lists

    Returns:
        _type_: _description_
    """
    if not isinstance(lst, list):
        return [lst]
    if len(lst) == 0:
        return lst

    # Flatten the list until there are no more nested lists
    while any(isinstance(i, list) for i in lst):
        new_lst = []
        for i in lst:
            if isinstance(i, list):
                new_lst.extend(i)
            else:
                new_lst.append(i)
        lst = new_lst
    return lst


def apply_percise_numbers(matrix):
    return [[most_accurate(elem) for elem in row] for row in matrix]
    

@debug_in_out(enabled=False)
def convert_element(x, bool_as_string = False):
    """_summary_
    converts an element to a numeric type if possible
    Args:
        x (_type_): _description_ element to convert from string to numeric type

    Returns:
        _type_: _description_ numeric type if possible, or a trimmed string
    """
    if not isinstance(x, str):
        x = str(x)
        # if "−" in x:
        #     x.replace("−", "-")
    x = x.strip()
    if isnum(x):
        try:
            floating = float(x)
            integer = int(floating)

            if floating == integer:
                return integer
            return floating
        except ValueError:
            pass
    else:
        
        if x == 'true' or x == 'True':
            return True
        elif x == 'false' or x == 'False':
            return False
        return x.strip('"\'')


def is_column_vector(x):
    """
    Column Vector Criteria:
    1. Object must be a list
    2. The object must have at least one element
    3. All elements must be lists
    4. All elements must have exactly one element
    """
    if not isinstance(x, list):
        return False
    if len(x) == 0:
        return False
    return all(isinstance(i, list) and len(i) == 1 for i in x)


def is_row_vector(x):
    """
    Row Vector Criteria:
    1. Object must be a list
    2. Object must have exactly one element
    3. The single element must be a list
    4. The single element must have at least one element
    """
    # Object must be a list
    if not isinstance(x, list):
        return False
    # object must have at least one element
    if len(x) != 1:
        return False
    if not isinstance(x[0], list):
        return False
    return len(x[0]) >= 1


def is_vector(x):
    return is_column_vector(x) or is_row_vector(x)


def to_row_vector(x):
    return [flatten(x)]


def to_col_vector(x):
    return [[elem] for elem in flatten(x)]


def all_numeric_elements(x):
    elements = flatten(x)
    elements = [convert_element(elem) for elem in elements]
    return all(isinstance(elem, (int, float)) for elem in elements)


def get_symbolic_indices(x):
    if not isinstance(x, list) or not x:
        return None

    indices = []
    for i in range(len(x)):
        if isinstance(x[i], list):
            for j in range(len(x[i])):
                elem = convert_element(x[i][j])
                if isinstance(elem, str):
                    indices.append((i, j))
    return indices


def is_matrix(x):
    if not isinstance(x, list) or not x:
        return False
    if not isinstance(x[0], list) or not x[0]:
        return
    # list comprehension
    return all(isinstance(row, list) and len(row) == len(x[0]) for row in x)


def reshape(mat, rows: int, cols: int, fill: int = 0):
    # Ensure mat is a list of lists
    if len(mat) > 0:
        if not isinstance(mat[0], list):
            mat = [mat]
    # Flatten the original matrix into a single list
    flat_list = flatten(mat)

    # Determine the number of rows and columns for the reshaped matrix
    rows = len(flat_list) // cols
    if len(flat_list) % cols != 0:
        rows += 1

    # Create the new matrix with the reshaped dimensions,
    # filling in values from the flattened list
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


def new_matrix(rows: int, cols: int, fill: int = 0):
    return [[fill for j in range(cols)] for i in range(rows)]


def get_matrix_dimensions(x):
    if not is_matrix(x):
        return None
    return Dimensions(len(x), len(x[0]))


def list_is_empty(x):
    return isinstance(x, list) and not x


def is_flat_list(x):
    return isinstance(x, list) and len(x) > 0 and not isinstance(x[0], list)


def identity_matrix(n):
    """
    Create an identity matrix of size n x n.
    
    Parameters:
    n (int): The number of rows and columns

    Returns:
    list of list of int/float: The identity matrix
    """
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def _perform_tests():
    col_vec = [[1], [2], [3]]
    row_vec = [[1, 2, 3]]
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    matrix_symbolic = [[1, 2, '6a'], [4, 5, 6], [7, '3b', 9]]

    # assert generic matrices
    assert is_matrix(matrix)
    assert is_matrix(col_vec)
    assert is_matrix(row_vec)

    # assert column vectors
    assert is_column_vector(col_vec)
    assert is_column_vector(row_vec) == False
    assert is_column_vector(matrix) == False

    # assert row vectors
    assert is_row_vector(row_vec)
    assert is_row_vector(col_vec) == False
    assert is_vector(matrix) == False

    # assert conversion to row vectors
    assert to_row_vector(col_vec) == row_vec

    # assert conversion to column vectors
    assert to_col_vector(row_vec) == col_vec

    # assert all numeric elements
    assert all_numeric_elements(matrix)
    assert all_numeric_elements(col_vec)
    assert all_numeric_elements(row_vec)

    # assert symbolic indices
    assert get_symbolic_indices(matrix_symbolic) == [(0, 2), (2, 1)]

    # assert matrix dimensions
    assert get_matrix_dimensions(matrix) == Dimensions(3, 3)
    assert get_matrix_dimensions(col_vec) == Dimensions(3, 1)
    assert get_matrix_dimensions(row_vec) == Dimensions(1, 3)

    print("{}: All tests passed!".format(__file__.split('\\')[-1]))


if __name__ == '__main__':
    _perform_tests()
