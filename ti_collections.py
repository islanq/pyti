
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

