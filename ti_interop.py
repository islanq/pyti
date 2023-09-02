import sys
if sys.platform == 'win32':
    from ti_numbers.frac import Frac
    from ti_polyfill.polyfill import is_numeric, is_digit
elif sys.platform == 'TI-Nspire':
    from frac import Frac
    from polyfill import is_numeric, is_digit
    from ti_system import readST, writeST
    

""" ti_system -----------------
    'clear',
    'clear_history',
    'clock',
    'disp_clr',
    'escape',
    'evalFunc',
    'eval_function',
    'floor',
    'getKey',
    'get_key',
    'get_mouse',
    'get_platform',
    'get_screen_dim',
    'get_time_ms',
    'get_use_buffer',
    'getmouse',
    'isFloat',
    'readST',
    'readSTLst',
    'readSTNum',
    'recall_list',
    'recall_value',
    'sleep_ms',
    'store_list'
    'store_value',
    'string_size',
    'ticks_ms',
    'use_buffer',
    'wait',
    'writeST',
    'writeSTLst'
"""

class TiReadWriteException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class Interop:
    
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
    
    def exec(cmd_str):
        try:
            return readST('expr("{}")'.format(cmd_str))
        except:
            pass
    
    @staticmethod
    def is_ti_list(ti_list_str):
        if not ti_list_str.startswith('{') and ti_list_str.endswith('}'):
            return False
        return all(s not in ti_list_str for s in [', ', ':'])
    
    @staticmethod
    def is_ti_mat(ti_mat_str):
        # ti mat will never contain ', ' or ':'
        if not ti_mat_str.startswith('[['):
            return False
        if not ti_mat_str.endswith(']]'):
            return False
        return all(s not in ti_mat_str for s in [', ', ':'])
       
    @staticmethod
    def is_py_list(py_list):
        return isinstance(py_list, list)
    
    @staticmethod
    def is_py_mat(py_list_of_list):
        # Ensure that it's a list of lists and that all lists have the same length
        if not isinstance(py_list_of_list, list):
            return False
        if not all(isinstance(row, list) for row in py_list_of_list):
            return False
        return all(len(row) == len(py_list_of_list[0]) for row in py_list_of_list)
    
    @staticmethod
    def is_ti_or_py_mat(mat_str):
        return mat_str.startswith('[[') and mat_str.endswith(']]') and not ', ' in mat_str and not '][' in mat_str
    
    @staticmethod
    def to_ti_list(py_list):
        return "{" + ",".join(map(str, py_list)) + "}"
    
    @staticmethod
    def to_ti_mat(py_list_of_list):
        return "[" + "".join(map(lambda row: Interop.to_ti_list(row).replace('{', '[').replace('}', ']'), py_list_of_list)) + "]"
    
    @staticmethod
    def to_py_list(ti_list_str):
        if isinstance(ti_list_str, list):
            return ti_list_str
        if Interop.is_ti_list(ti_list_str): #ti_list_str.startswith('{') and ti_list_str.endswith('}') and ':' not in ti_list_str:
            return [float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in ti_list_str[1:-1].split(",")]

    @staticmethod
    def to_py_mat(ti_mat_str):
        if isinstance(ti_mat_str, list):
            return ti_mat_str
        if not Interop.is_ti_mat(ti_mat_str):
            raise ValueError("Invalid ti matrix string: {}".format(ti_mat_str))
        if not '][' in ti_mat_str:
            ti_mat_str = ti_mat_str[2:-2]
            return [[float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in ti_mat_str.split(",")]]
        else:
            return [[float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in row.split(",")] for row in ti_mat_str[2:-2].split("][")]

    @staticmethod
    def is_col_vec(matrix):
        if isinstance(matrix, list):
            return all(isinstance(row, list) and len(row) == 1 for row in matrix)
        elif isinstance(matrix, str) and Interop.is_ti_mat(matrix):
            return Interop.is_col_vec(Interop.to_py_mat(matrix))
        return False
            
    @staticmethod
    def is_row_vec(matrix):
        if isinstance(matrix, list):
            return len(matrix) == 1
        elif isinstance(matrix, str) and Interop.is_ti_mat(matrix):
            return Interop.is_row_vec(Interop.to_py_mat(matrix))
        return False
    