import sys
import re
if sys.platform == 'win32':
    from lib.polyfill import is_numeric, is_digit
    from lib.frac import Frac
else:
    from ti_system import readST, writeST
    from eval_expr import eval_expr, call_func
    from ti_interop import tiexec
    from polyfill import is_numeric, is_digit


_py_lst_re = re.compile(r'^\[(?!\[).*\]$')
_py_mat_re = re.compile(r'^\[\[(?!.*,(?![ ])).*\]\]$')

def convert_element(x):
    if not isinstance(x, str):
        x = str(x)
        if "−" in x:
            x.replace("−", "-")
    if is_numeric(x):
        try:
            return int(x) if int(x) == float(x) else float(x)
        except ValueError:
            pass
    else:
        return x.strip('"\'')
            
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
    
    def tiexec(self, cmd_str_or_func_name, *args):
        from ti_interop import tiexec
        return tiexec(cmd_str_or_func_name, *args)


    @staticmethod
    def is_py_col_vec(matrix) -> bool:
        if isinstance(matrix, list):
            return all(isinstance(row, list) and len(row) == 1 for row in matrix)
        return False

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
        if not (py_list_str.startswith('[') and py_list_str.endswith(']')):
            return False
        return all(s not in py_list_str for s in [', ', ':'])

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
    def ti_list_to_mat(ti_list_str, elements_per_row = 1) -> str: 
        if not TiCollections.is_ti_list(ti_list_str):
            raise ValueError("Invalid ti list string: {}".format(ti_list_str))
        return TiCollections.tiexec("list@>mat({}, {})".format(ti_list_str, elements_per_row))


    @staticmethod
    def is_py_list(py_list) -> bool:
        return isinstance(py_list, list)
    
    @staticmethod
    def is_py_list_str(py_list_str) -> bool:
        if not isinstance(py_list_str, str):
            return False
        if re.match(_py_lst_re, py_list_str.strip()) is None:
            return False
        return True

    @staticmethod
    def is_py_mat_str(py_mat_str) -> bool:
        if not isinstance(py_mat_str, str):
            return False
        if re.match(_py_mat_re, py_mat_str.strip()) is None:
            return False
        return True


    @staticmethod
    def py_str_to_list(ti_list_str) -> list:
        if isinstance(ti_list_str, list):
            return ti_list_str
        if not TiCollections.is_py_list_str(ti_list_str):
            raise ValueError("Invalid ti list string: {}".format(ti_list_str))
        return [convert_element(x.strip()) for x in ti_list_str[1:-1].split(",")]
    
    @staticmethod
    def py_str_to_mat2(ti_mat_str) -> list:
        if isinstance(ti_mat_str, list):
            return ti_mat_str
        if not TiCollections.is_py_mat_str(ti_mat_str):
            raise ValueError("Invalid ti matrix string: {}".format(ti_mat_str))
        # Helper function to process a row string and return a list of processed elements
        def process_row(row_str):
            return [convert_element(x.strip()) for x in row_str.split(",")]
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
                convert_element(x.strip()) for x in row.split(",")
            ] 
            for row in ti_mat_str[2:-2].split("], [")
        ]
    
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
    def to_py_list(ti_list_str) -> list:
        if isinstance(ti_list_str, list):
            return ti_list_str
        if TiCollections.is_ti_list(ti_list_str): 
            return [convert_element(x.strip()) for x in ti_list_str[1:-1].split(",")]

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
    def to_py_mat(ti_mat_str) -> list:
        if isinstance(ti_mat_str, list):
            return ti_mat_str
        if not TiCollections.is_ti_mat(ti_mat_str):
            raise ValueError("Invalid ti matrix string: {}".format(ti_mat_str))
        # Helper function to process a row string and return a list of processed elements
        def process_row(row_str):
            return [convert_element(x.strip().replace("−", "-")) for x in row_str.split(",")]
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
    def to_ti_row_vec(matrix) -> str:
        if TiCollections.is_ti_row_vec(matrix):
            return matrix
        return TiCollections.to_ti_mat(TiCollections.to_py_row_vec(matrix))
    
    
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

py_lst_str = str( [1,2,3,4,1,'h',3,4] )
py_mat_str = str( [[1,2,3,4],[1,'h',-3,4]] )
ti_mat_str = "[[1,-2,3,4][1,h,3,4]]"
print(py_mat_str)
print(py_lst_str)




assert (_py_mat_re.match(py_mat_str) is not None)
assert (_py_mat_re.match(py_lst_str) is None)
assert (_py_mat_re.match(ti_mat_str) is None)

assert (_py_lst_re.match(py_lst_str) is not None)
assert (_py_lst_re.match(py_mat_str) is None)
assert (_py_lst_re.match(ti_mat_str) is None)



print(TiCollections.py_str_to_mat(py_mat_str))
