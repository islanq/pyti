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

class Interoperability:
    
    
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
    
    def is_ti_list(ti_list_str):
        return ti_list_str.startswith('{') and ti_list_str.endswith('}')
    
    def is_ti_mat(ti_mat_str):
        return all(s in ti_mat_str for s in ['][','[[' , ']]'])
    
    def is_ti_or_py_mat(mat_str):
        return mat_str.startswith('[[') and mat_str.endswith(']]') and not ', ' in mat_str and not '][' in mat_str
    
    @staticmethod
    def to_ti_list(py_list):
        return "{" + ",".join(map(str, py_list)) + "}"
    
    @staticmethod
    def to_ti_mat(py_list_of_list):
        return "[" + "".join(map(lambda row: Interoperability.to_ti_list(row).replace('{', '[').replace('}', ']'), py_list_of_list)) + "]"
    
    @staticmethod
    def to_py_list(ti_list_str):
        if ti_list_str.startswith('{') and ti_list_str.endswith('}') and ':' not in ti_list_str:
            return [float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in ti_list_str[1:-1].split(",")]

    @staticmethod
    def to_py_mat(ti_mat_str):
        if all(s in ti_mat_str for s in ['][','[[' , ']]']) and ti_mat_str.startswith('[[') and ti_mat_str.endswith(']]'):
            return [[float(x.replace("−", "-")) if is_numeric(x) else int(x.replace("−", "-")) if is_digit(x) else x.strip() for x in row.split(",")] for row in ti_mat_str[2:-2].split("][")]

    
"""        
    @staticmethod
    def to_py_list(ti_list_str):
        if ti_list_str.startswith('{') and ti_list_str.endswith('}') and ':' not in ti_list_str:
            return [float(x) if is_numeric(x.replace(".", "")) else x.strip() for x in ti_list_str[1:-1].split(",")]

    @staticmethod
    def to_py_mat(ti_mat_str):
        if all(s in ti_mat_str for s in ['][','[[' , ']]']) and ti_mat_str.startswith('[[') and ti_mat_str.endswith(']]'):
            return [[float(x) if is_numeric(x.replace(".", "")) else x.strip() for x in row.split(",")] for row in ti_mat_str[2:-2].split("][")]"""
        

        


print(Interoperability.to_ti_list([1,2,-3,4, 'x']))
print(Interoperability.to_ti_mat([[1,2,3,-4],[1,'h',3,4]]))

print(Interoperability.to_py_list("{1,2,3,4,1,h,3,4}"))
print(Interoperability.to_py_mat("[[1,-2,3,4][1,h,3,4]]"))
# print(Interoperability.is_ti_mat("[[1,2,3,4][1,h,3,4]]"))
# print(Interoperability.is_py_mat("[[1,2,3,4][1,h,3,4]]"))






