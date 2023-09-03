import sys
if sys.platform == 'win32':
    from lib.frac import Frac
    from lib.ti_polyfill import is_numeric, is_digit
elif sys.platform == 'TI-Nspire':
    from frac import Frac
    from polyfill import is_numeric, is_digit
    from ti_system import readST, writeST
    from eval_expr import eval_expr, call_func

class TiReadWriteException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class TiInterop:
    
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
    
    def exec(self, cmd_str_or_func_name, *args):
        return exec(cmd_str_or_func_name, *args)

    @staticmethod
    def is_ti_list(ti_list_str):
        if not isinstance(ti_list_str, str):
            return False
        if not (ti_list_str.startswith('{') and ti_list_str.endswith('}')):
            return False
        return all(s not in ti_list_str for s in [', ', ':'])
    
    @staticmethod
    def is_ti_mat(ti_mat_str):
        # ti mat will never contain ', ' or ':'
        if not isinstance(ti_mat_str, str):
            return False
        if not ti_mat_str.startswith('[['):
            return False
        if not ti_mat_str.endswith(']]'):
            return False
        return all(s not in ti_mat_str for s in [', ', ':'])
       
    @staticmethod
    def is_ti_row_vec(ti_mat_str):
        
        return TiInterop.is_ti_mat(ti_mat_str) and not '][' in ti_mat_str 
    
    @staticmethod
    def is_ti_col_vec(ti_mat_str):
        if not (TiInterop.is_ti_mat(ti_mat_str) and '][' in ti_mat_str):
            return False
        return TiInterop.is_py_col_vec(TiInterop.to_py_mat(ti_mat_str))
       
    @staticmethod
    def is_py_list(py_list):
        return isinstance(py_list, list)
    
    @staticmethod
    def is_py_mat(py_list):
        if not isinstance(py_list, list): # it's not a list
            return False
        if len(py_list) == 0: # it contains no rows, therefore not a matrix
            return False
        if not all(isinstance(row, list) for row in py_list): # all list rows
            return False
        return all(len(row) == len(py_list[0]) for row in py_list) # all rows == len
    
    @staticmethod
    def to_ti_list(py_list):
        if TiInterop.is_ti_list(py_list):
            return py_list
        return "{" + ",".join(map(str, py_list)) + "}"
    
    @staticmethod
    def to_ti_mat(py_list):
        if TiInterop.is_ti_mat(py_list):
            return py_list
        return "[" + "".join(map(lambda row: TiInterop.to_ti_list(row).replace('{', '[').replace('}', ']'), py_list)) + "]"
    
    @staticmethod
    def to_py_list(ti_list_str):
        if isinstance(ti_list_str, list):
            return ti_list_str
        if TiInterop.is_ti_list(ti_list_str): #ti_list_str.startswith('{') and ti_list_str.endswith('}') and ':' not in ti_list_str:
            return [float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in ti_list_str[1:-1].split(",")]

    @staticmethod
    def is_reg_py_list(py_list):
        if not isinstance(py_list, list):
            return False
        return not all(isinstance(item, list) for item in py_list)
    
    @staticmethod
    def to_py_mat(ti_mat_str):
        if isinstance(ti_mat_str, list):
            return ti_mat_str
        if not TiInterop.is_ti_mat(ti_mat_str):
            raise ValueError("Invalid ti matrix string: {}".format(ti_mat_str))
        if not '][' in ti_mat_str:
            ti_mat_str = ti_mat_str[2:-2]
            return [[float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in ti_mat_str.split(",")]]
        else:
            return [[float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in row.split(",")] for row in ti_mat_str[2:-2].split("][")]

    @staticmethod
    def to_ti_col_vec(matrix):
        if TiInterop.is_ti_col_vec(matrix):
            return matrix
        return TiInterop.to_ti_mat(TiInterop.to_py_col_vec(matrix))
    
    @staticmethod
    def to_py_col_vec(matrix):
        if TiInterop.is_py_col_vec(matrix):
            return matrix
        elif TiInterop.is_reg_py_list(matrix):
            return [[item] for item in matrix]
        elif TiInterop.is_ti_list(matrix):
            return TiInterop.to_py_col_vec(TiInterop.to_py_list(matrix))
        elif TiInterop.is_py_row_vec(matrix):
            return TiInterop.to_py_col_vec(TiInterop.flatten(matrix))
        elif TiInterop.is_ti_row_vec(matrix):
            return TiInterop.to_py_col_vec(TiInterop.to_py_mat(matrix))
        raise ValueError("Cannot convert to column vec: {}".format(matrix))
    
    @staticmethod
    def to_py_row_vec(matrix):
        if TiInterop.is_py_row_vec(matrix):
            return matrix
        elif TiInterop.is_reg_py_list(matrix):
            return [matrix]
        elif TiInterop.is_ti_list(matrix):
            return TiInterop.to_py_row_vec(TiInterop.to_py_list(matrix))
        elif TiInterop.is_py_col_vec(matrix) or TiInterop.is_ti_col_vec(matrix):
            return TiInterop.to_py_row_vec(TiInterop.flatten(matrix))
        elif TiInterop.is_ti_row_vec(matrix):
            return TiInterop.to_py_row_vec(TiInterop.to_py_mat(matrix))
        raise ValueError("Cannot convert to row vec: {}".format(matrix))
                       
    @staticmethod
    def is_py_row_vec(matrix):
        if isinstance(matrix, list):
            return len(matrix) == 1 and isinstance(matrix[0], list)
        return False
    
    @staticmethod
    def is_py_col_vec(matrix):
        if isinstance(matrix, list):
            return all(isinstance(row, list) and len(row) == 1 for row in matrix)
        return False
    
    @staticmethod
    def flatten(lst):
        """Flatten a list of lists into a single list."""
        return [item for sublist in lst for item in (TiInterop.flatten(sublist) if isinstance(sublist, list) else [sublist])]
    
    @staticmethod
    def is_equality(expression: str):
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

def exec(cmd_str_or_func_name, *args):
    if len(args) > 0:
        try:
            return call_func(cmd_str_or_func_name, *args)
        except:
            pass
    try:
        return eval_expr(cmd_str_or_func_name)
    except:
        pass
    try:
        return readST(cmd_str_or_func_name)
    except:
        pass
    try:
        return readST('expr("{}")'.format(cmd_str_or_func_name))
    except:
        pass