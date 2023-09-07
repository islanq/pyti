import sys

if sys.platform == 'win32':
    from lib.polyfill import is_numeric, is_digit
    from lib.frac import Frac
else:
    from ti_system import readST, writeST
    from eval_expr import eval_expr, call_func
    from ti_interop import tiexec
    from polyfill import is_numeric, is_digit

from ti_interop import tiexec, TiType

class TiReadWriteException(Exception):
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
        
    
    def save_ti_var(name, value):
        try: 
            writeST(name, value)
        except TiReadWriteException as e:
            print("error saving variable: {}".format(e.message))
    
    def load_ti_var(name):
        try:
            return readST(name)
        except TiReadWriteException as e:
            print("error loading variable: {}".format(e.message))
    
    def tiexec(self, cmd_str_or_func_name, *args):
        return tiexec(cmd_str_or_func_name, *args)

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
    def is_ti_col_vec(ti_mat_str) -> bool:
        if not (TiCollections.is_ti_mat(ti_mat_str) and '][' in ti_mat_str):
            return False
        return TiCollections.is_py_col_vec(TiCollections.to_py_mat(ti_mat_str))
       
    @staticmethod
    def is_py_list(py_list) -> bool:
        return isinstance(py_list, list)
    
    @staticmethod
    def is_py_mat(py_list) -> bool:
        if not isinstance(py_list, list): # it's not a list
            return False
        if len(py_list) == 0: # it contains no rows, therefore not a matrix
            return False
        if not all(isinstance(row, list) for row in py_list): # all list rows
            return False
        return all(len(row) == len(py_list[0]) for row in py_list) # all rows == len
    
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
    def to_py_list(ti_list_str) -> list:
        if isinstance(ti_list_str, list):
            return ti_list_str
        if TiCollections.is_ti_list(ti_list_str): 
            return [float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in ti_list_str[1:-1].split(",")]

    @staticmethod
    def is_reg_py_list(py_list) -> bool:
        if not isinstance(py_list, list):
            return False
        return not all(isinstance(item, list) for item in py_list)
    
    @staticmethod
    def to_py_mat(ti_mat_str) -> list:
        if isinstance(ti_mat_str, list):
            return ti_mat_str
        if not TiCollections.is_ti_mat(ti_mat_str):
            raise ValueError("Invalid ti matrix string: {}".format(ti_mat_str))
        if not '][' in ti_mat_str:
            ti_mat_str = ti_mat_str[2:-2]
            return [[float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in ti_mat_str.split(",")]]
        else:
            return [[float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in row.split(",")] for row in ti_mat_str[2:-2].split("][")]

    @staticmethod
    def to_ti_col_vec(matrix) -> str:
        if TiCollections.is_ti_col_vec(matrix):
            return matrix
        return TiCollections.to_ti_mat(TiCollections.to_py_col_vec(matrix))
    
    @staticmethod
    def to_ti_row_vec(matrix) -> str:
        if TiCollections.is_ti_row_vec(matrix):
            return matrix
        return TiCollections.to_ti_mat(TiCollections.to_py_row_vec(matrix))
    
    @staticmethod
    def to_py_col_vec(matrix) -> list:
        if TiCollections.is_py_col_vec(matrix):
            return matrix
        elif TiCollections.is_reg_py_list(matrix):
            return [[item] for item in matrix]
        elif TiCollections.is_ti_list(matrix):
            return TiCollections.to_py_col_vec(TiCollections.to_py_list(matrix))
        elif TiCollections.is_py_row_vec(matrix):
            return TiCollections.to_py_col_vec(TiCollections.flatten(matrix))
        elif TiCollections.is_ti_row_vec(matrix):
            return TiCollections.to_py_col_vec(TiCollections.to_py_mat(matrix))
        elif TiCollections.is_py_mat(matrix):
            return TiCollections.to_py_col_vec(TiCollections.flatten(matrix))
        raise ValueError("Cannot convert to column vec: {}".format(matrix))
    
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
    def is_py_row_vec(matrix) -> bool:
        if isinstance(matrix, list):
            return len(matrix) == 1 and isinstance(matrix[0], list)
        return False
    
    @staticmethod
    def is_py_col_vec(matrix) -> bool:
        if isinstance(matrix, list):
            return all(isinstance(row, list) and len(row) == 1 for row in matrix)
        return False
    
    @staticmethod
    def flatten(lst) -> list:
        """Flatten a list of lists into a single list."""
        return [item for sublist in lst for item in (TiCollections.flatten(sublist) if isinstance(sublist, list) else [sublist])]
    
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
    def ti_list_to_mat(ti_list_str, elements_per_row = 1) -> str: 
        if not TiCollections.is_ti_list(ti_list_str):
            raise ValueError("Invalid ti list string: {}".format(ti_list_str))
        return TiCollections.tiexec("list@>mat({}, {})".format(ti_list_str, elements_per_row))
