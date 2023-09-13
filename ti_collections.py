
import sys
if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../', '.'])
else:
    from ti_system import readST, writeST
    from eval_expr import eval_expr, call_func
    # from ti_interop import tiexec
    
from polyfill import is_numeric, is_digit
from collections import namedtuple
from ti_interop import tiexec
from ti_traits import TraitsReport, is_type
from ti_converters import *
from dummy_types import *


class UnconvertableString(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class TiCollections:

    def __init__(self):
        for method_name in dir(TiCollections):
            method = getattr(TiCollections, method_name)
            if callable(method) and isinstance(method, staticmethod):
                method = method.__func__  # Get the actual function
                setattr(self, method_name, method.__get__(self))

    @staticmethod
    def is_py_col_vec(matrix) -> bool:
        return is_type(matrix, PyColVec)

    @staticmethod
    def is_py_mat(py_list) -> bool:
        return is_type(py_list, PyMat, usesub=True)

    @staticmethod
    def is_py_row_vec(matrix) -> bool:
        return is_type(matrix, PyRowVec)

    @staticmethod
    def is_reg_py_list(py_list) -> bool:
        return is_type(py_list, PyList)

    @staticmethod
    def is_reg_py_list_str(py_list_str) -> bool:
        return is_type(py_list_str, PyStrList)

    @staticmethod
    def is_ti_col_vec(ti_mat_str) -> bool:
        return is_type(ti_mat_str, TiColVec)

    @staticmethod
    def is_ti_list(ti_list_str) -> bool:
        return is_type(ti_list_str, TiList)

    @staticmethod
    def is_ti_mat(ti_mat_str) -> bool:
        return is_type(ti_mat_str, TiMat)

    @staticmethod
    def is_ti_row_vec(ti_mat_str) -> bool:
        return is_type(ti_mat_str, TiRowVec)

    @staticmethod
    def is_py_list(py_list) -> bool:
        return is_type(py_list, PyList)

    @staticmethod
    def is_py_list_str(py_list_str) -> bool:
        return is_type(py_list_str, PyStrList)

    @staticmethod
    def is_py_mat_str(py_mat_str) -> bool:
        return is_type(py_mat_str, PyStrMat)


    @staticmethod
    def to_ti_list(py_list) -> str:
        return to_ti_list(py_list)

    @staticmethod
    def to_ti_mat(py_list) -> str:
        return to_ti_mat(py_list)
    
    @staticmethod
    def to_py_mat(ti_list_str, elements_per_row: int = None, fill: int = 0) -> str:
        return to_py_mat(ti_list_str, elements_per_row, fill)
    
    @staticmethod
    def to_py_list(ti_list_str) -> list:
        return to_py_list(ti_list_str)
    
    @staticmethod
    def to_py_col_vec(matrix) -> list:
        return to_py_mat(matrix, 1)
    
    @staticmethod
    def to_py_row_vec(matrix) -> list:
        return to_py_mat(matrix, 1)



"""
    @staticmethod
    def is_py_col_vec(matrix) -> bool:
        if isinstance(matrix, list):
            return all(isinstance(row, list) and len(row) == 1 for row in matrix)
        return False

    @staticmethod
    def is_py_mat(py_list) -> bool:
        if not isinstance(py_list, list):  # it's not a list
            return False
        if len(py_list) == 0:  # it contains no rows, therefore not a matrix
            return False
        if not all(isinstance(row, list) for row in py_list):  # all list rows
            return False
        # all rows == len
        return all(len(row) == len(py_list[0]) for row in py_list)

    @staticmethod
    def is_py_row_vec(matrix) -> bool:
        if isinstance(matrix, list):
            return len(matrix) == 1 and isinstance(matrix[0], list)
        return False

    @staticmethod
    def is_reg_py_list(py_list) -> bool:
        if not isinstance(py_list, list):
            return False
        return not all(isinstance(item, list) for item in py_list)

    @staticmethod
    def is_reg_py_list_str(py_list_str) -> bool:
        if not isinstance(py_list_str, str):
            return False
        if not py_list_str.startswith('[') or not py_list_str.endswith(']'):
            return False
        if '][' in py_list_str:
            return False
        return not ':' in py_list_str

    @staticmethod
    def is_ti_col_vec(ti_mat_str) -> bool:
        if not (TiCollections.is_ti_mat(ti_mat_str) and '][' in ti_mat_str):
            return False
        return TiCollections.is_py_col_vec(TiCollections.to_py_mat(ti_mat_str))

    @staticmethod
    def is_ti_list(ti_list_str) -> bool:
        if not isinstance(ti_list_str, str):
            return False
        if not (ti_list_str.startswith('{') and ti_list_str.endswith('}')):
            return False
        return all(s not in ti_list_str for s in [', ', ':'])

    @staticmethod
    def is_ti_mat(ti_mat_str) -> bool:
        # ti mat will never contain ', ' or ':'
        if not isinstance(ti_mat_str, str):
            return False
        if not ti_mat_str.startswith('[['):
            return False
        if not ti_mat_str.endswith(']]'):
            return False
        return all(s not in ti_mat_str for s in [', ', ':'])

    @staticmethod
    def is_ti_row_vec(ti_mat_str) -> bool:
        return TiCollections.is_ti_mat(ti_mat_str) and not '][' in ti_mat_str

    @staticmethod
    def ti_list_to_mat(ti_list_str, elements_per_row=1) -> str:

        if not TiCollections.is_ti_list(ti_list_str):
            raise ValueError("Invalid ti list string: {}".format(ti_list_str))
        return tiexec("list@>mat({}, {})".format(ti_list_str, elements_per_row))

    @staticmethod
    def is_py_list(py_list) -> bool:
        return isinstance(py_list, list)

    @staticmethod
    def is_py_list_str(py_list_str) -> bool:
        if not isinstance(py_list_str, str):
            return False
        if TiCollections.is_ti_list(py_list_str):
            return False
        if not py_list_str.startswith("["):
            return False
        if not py_list_str.endswith("]"):
            return False
        if ", " in py_list_str:
            return True

    @staticmethod
    def is_py_mat_str(py_mat_str) -> bool:
        if not isinstance(py_mat_str, str):
            return False
        if TiCollections.is_ti_mat(py_mat_str):
            return False
        if not py_mat_str.startswith("[["):
            return False
        if not py_mat_str.endswith("]]"):
            return False
        if ", " in py_mat_str:
            return True

    @staticmethod
    def is_equality(expression: str) -> bool:
        if not isinstance(expression, str):
            return False
        if "=" not in expression and "==" not in expression:
            return False
        if expression.count("=") > 1 or expression.count("==") > 1:
            return False
        if "==" in expression:
            lhs, rhs = expression.split("==", 1)
        else:
            lhs, rhs = expression.split("=", 1)
        return not (lhs.strip() == "" and rhs.strip() == "")

    @staticmethod
    def is_py_mat(py_list) -> bool:
        if not isinstance(py_list, list):  # it's not a list
            return False
        if len(py_list) == 0:  # it contains no rows, therefore not a matrix
            return False
        if not all(isinstance(row, list) for row in py_list):  # all list rows
            return False
        # all rows == len
        return all(len(row) == len(py_list[0]) for row in py_list)

    @staticmethod
    def py_str_to_list(ti_list_str) -> list:
        if isinstance(ti_list_str, list):
            return ti_list_str
        if not TiCollections.is_py_list_str(ti_list_str):
            raise ValueError("Invalid ti list string: {}".format(ti_list_str))
        return [_convert_element(x.strip()) for x in ti_list_str[1:-1].split(",")]

    @staticmethod
    def py_str_to_mat2(ti_mat_str) -> list:
        if isinstance(ti_mat_str, list):
            return ti_mat_str
        if not TiCollections.is_py_mat_str(ti_mat_str):
            raise ValueError("Invalid ti matrix string: {}".format(ti_mat_str))
        # Helper function to process a row string and return a list of processed elements

        def process_row(row_str):
            return [_convert_element(x.strip()) for x in row_str.split(",")]
        # Remove outermost brackets and split the string into individual row strings
        row_strs = ti_mat_str[2:-2].split("], [")
        # Process each row string and return the list of processed rows
        return [process_row(row_str) for row_str in row_strs]

    @staticmethod
    def py_str_to_mat(ti_mat_str) -> list:
        if isinstance(ti_mat_str, list):
            return ti_mat_str
        if not TiCollections.is_py_mat_str(ti_mat_str):
            raise ValueError("Invalid ti matrix string: {}".format(ti_mat_str))
        return [
            [
                _convert_element(x.strip()) for x in row.split(",")
            ]
            for row in ti_mat_str[2:-2].split("], [")
        ]

    @staticmethod
    def to_py_list(ti_list_str) -> list:
        if isinstance(ti_list_str, list):
            return ti_list_str
        elif TiCollections.is_ti_list(ti_list_str):
            return [_convert_element(x.strip()) for x in ti_list_str[1:-1].split(",")]
        elif TiCollections.is_py_list_str(ti_list_str):
            return TiCollections.py_str_to_list(ti_list_str)
        raise UnconvertableString(
            "Cannot convert to list: {}".format(ti_list_str))

    @staticmethod
    def to_py_col_vec(matrix) -> list:
        tic = TiCollections
        if tic.is_py_col_vec(matrix):
            return matrix

        elif tic.is_reg_py_list(matrix):
            return [[item] for item in matrix]

        elif tic.is_ti_list(matrix):
            return tic.to_py_col_vec(tic.to_py_list(matrix))

        elif tic.is_py_row_vec(matrix):
            return tic.to_py_col_vec(tic.flatten(matrix))

        elif tic.is_ti_row_vec(matrix):
            return tic.to_py_col_vec(tic.to_py_mat(matrix))

        elif tic.is_py_mat(matrix):
            return tic.to_py_col_vec(tic.flatten(matrix))

        raise ValueError("Cannot convert to column vec: {}".format(matrix))

    @staticmethod
    def to_py_mat(ti_mat_str) -> list:
        if isinstance(ti_mat_str, list):
            return ti_mat_str
        if not TiCollections.is_ti_mat(ti_mat_str):
            raise ValueError("Invalid ti matrix string: {}".format(ti_mat_str))
        # Helper function to process a row string and return a list of processed elements

        def process_row(row_str):
            return [_convert_element(x.strip().replace("−", "-")) for x in row_str.split(",")]
        # Remove outermost brackets and split the string into individual row strings
        row_strs = ti_mat_str[2:-2].split("], [")
        # Process each row string and return the list of processed rows
        return [process_row(row_str) for row_str in row_strs]

    @staticmethod
    def to_py_row_vec(matrix) -> list:
        if TiCollections.is_py_row_vec(matrix):
            return matrix

        elif TiCollections.is_reg_py_list(matrix):
            return [matrix]

        elif TiCollections.is_ti_list(matrix):
            return TiCollections.to_py_row_vec(TiCollections.to_py_list(matrix))

        elif TiCollections.is_py_col_vec(matrix) or TiCollections.is_ti_col_vec(matrix):
            return TiCollections.to_py_row_vec(TiCollections.flatten(matrix))

        elif TiCollections.is_ti_row_vec(matrix):
            return TiCollections.to_py_row_vec(TiCollections.to_py_mat(matrix))

        elif TiCollections.is_py_mat(matrix):
            return TiCollections.to_py_row_vec(TiCollections.flatten(matrix))

        raise ValueError("Cannot convert to row vec: {}".format(matrix))

    @staticmethod
    def to_ti_col_vec(matrix) -> str:
        if TiCollections.is_ti_col_vec(matrix):
            return matrix
        return TiCollections.to_ti_mat(TiCollections.to_py_col_vec(matrix))

    @staticmethod
    def to_ti_list(py_list) -> str:
        if TiCollections.is_ti_list(py_list):
            return py_list
        return "{" + ",".join(map(str, py_list)) + "}"

    @staticmethod
    def to_ti_mat(py_list) -> str:
        if TiCollections.is_ti_mat(py_list):
            return py_list
        return "[" + "".join(map(lambda row: TiCollections.to_ti_list(row).replace('{', '[').replace('}', ']'), py_list)) + "]"

    @staticmethod
    def to_ti_row_vec(matrix: list) -> str:
        if TiCollections.is_ti_row_vec(matrix):
            return matrix
        return TiCollections.to_ti_mat(TiCollections.to_py_row_vec(matrix))

    @staticmethod
    def flatten(lst: list) -> list:
        #Flatten a list of lists into a single list.
        return [item for sublist in lst for item in (TiCollections.flatten(sublist) if isinstance(sublist, list) else [sublist])]


"""
