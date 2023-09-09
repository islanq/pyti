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


_py_lst_pat = r'^\[\[.*\]\]$'
_py_lst_re = re.compile(_py_lst_pat)
#_py_mat_re = re.compile(r'^\[\[(?!.*,(?![ ])).*\]\]$')
#_py_mat_re = re.compile(r'^\[\[.*\]\]$')
_py_mat_re = re.compile(r'^\[\[.*(, ?).*\]\]$')

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

class UnconvertableString(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
         
class TiReadWriteException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
        

from collections import namedtuple

Dimensions = namedtuple('Dimensions', ['rows', 'cols'])
        
class _Converter:
    def to_list(self, obj):
        raise NotImplementedError("Subclasses must implement this method")
    def to_mat(self, obj):
        raise NotImplementedError("Subclasses must implement this method")
    def to_row_vec(self, obj):
        raise NotImplementedError("Subclasses must implement this method")
    def to_col_vec(self, obj):
        raise NotImplementedError("Subclasses must implement this method")

class _Traits:
    def is_list(self, obj) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    def is_mat(self, obj) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    def is_vec(self, obj) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    def is_col_vec(self, obj) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    def is_row_vec(self, obj) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    def dim(self, obj) -> Dimensions:
        raise NotImplementedError("Subclasses must implement this method")

# implemented
class TiStringTraits(_Traits):
    
    def is_list(self, string) -> bool:
        if not isinstance(string, str):
            return False
        if not (string.startswith('{') and string.endswith('}')):
            return False
        return all(s not in string for s in [', ', ':'])
    
    def is_mat(self, string) -> bool:
        # ti mat will never contain ', ' or ':'
        if not isinstance(string, str):
            return False
        if not string.startswith('[['):
            return False
        if not string.endswith(']]'):
            return False
        return not any(s in string for s in [', ', ':'])
    
    def is_vec(self, string) -> bool:
        return self.is_row_vec(string) or self.is_col_vec(string)
    
    def is_col_vec(self, string) -> bool:
        # [[1][2][3]]
        # it is a ti mat
        if not self.is_mat(string):
            return False
        # it must contain row separator
        if not '][' in string:
            return False
        return not ',' in string
    
    def is_row_vec(self, string) -> bool:
        # [[1,2,3]]
        if not self.is_mat(string):
            return False
        if '][' in string:
            return False
        return ',' in string
    
    def dim(self, string):
        row_separators = string.count('][')
        commas = string.count(',')
        num_rows = row_separators + 1
        num_cols = commas // num_rows + 1
        return Dimensions(num_rows, num_cols)

# implemented
class PyStringTraits(_Traits):
    
    def is_list(self, py_list_str):
        if not isinstance(py_list_str, str):
            return False
        if TiStringTraits.is_list(py_list_str):
            return False
        if not py_list_str.startswith("["):
            return False
        if not py_list_str.endswith("]"):
            return False
        return True
        
    def is_mat(self, mat_str):
        if not isinstance(mat_str, str):
            return False
        if TiStringTraits.is_mat(mat_str):
            return False
        if not mat_str.startswith("[["):
            return False
        if not  mat_str.endswith("]]"):
            return False
        return True
    
    def is_vec(self, obj):
        return self.is_col_vec(obj) or self.is_row_vec(obj)
    
    def is_col_vec(self, string):
        # [[1], [2], [3]]
        # it is a ti mat
        if not self.is_mat(string):
            return False
        # it must contain row separator
        return any(s for s in ['], [', '],['])
    
    def is_row_vec(self, string):
        # [[1,2,3]]
        if not self.is_mat(string):
            return False
        if '], [' in string:
            return False
        return ',' in string
    
    def dim(matrix_str) -> Dimensions:
        # Check for the special case of an empty list of lists
        if matrix_str == "[[]]":
            return 1, 0
        # Replacing '],[' with a marker to differentiate it from other commas
        if '], [' in matrix_str:
            matrix_str = matrix_str.replace('], [', '];[')
        else:
            matrix_str = matrix_str.replace('],[', '];[')
        # Count the number of row separators and commas in the string
        row_separators = matrix_str.count('];[')
        commas = matrix_str.count(',')
        # Calculate the number of rows and columns based on the counts
        num_rows = row_separators + 1
        num_cols = commas // num_rows + 1
        return Dimensions(num_rows, num_cols)

# implemented
class PyTraits(_Traits):
    
    def is_list(self, obj) -> bool:
        return isinstance(obj, list)
    
    def is_mat(self, py_list) -> bool:
        if not isinstance(py_list, list): # it's not a list
            return False
        if len(py_list) == 0: # it contains no rows, therefore not a matrix
            return False
        if not all(isinstance(row, list) for row in py_list): # all list rows
            return False
        return all(len(row) == len(py_list[0]) for row in py_list) # all rows == len
    
    def is_vec(self, matrix) -> bool:
        return (self.is_row_vec(matrix)
             or self.is_col_vec(matrix))
    
    def is_col_vec(self, matrix) -> bool:
        if isinstance(matrix, list):
            return all(isinstance(row, list)
               and len(row) == 1 for row in matrix)
        return False
    
    def is_row_vec(self, matrix) -> bool:
        if isinstance(matrix, list):
            return len(matrix) == 1 and isinstance(matrix[0], list)
        return False
    
    def dim(self, matrix):
        return Dimensions(len(matrix), len(matrix[0]))
    
   
    
    
    
class TiConverter(_Converter):
    def to_list(self, obj):
        return TiCollections.to_py_list(obj)
    def to_mat(self, obj):
        return TiCollections.to_py_mat(obj)
    def to_row_vec(self, obj):
        return TiCollections.to_py_row_vec(obj)
    def to_col_vec(self, obj):
        return TiCollections.to_py_col_vec(obj)
    
class PyConverter(_Converter):
    def to_list(self, obj):
        return TiCollections.to_py_list(obj)
    def to_mat(self, obj):
        return TiCollections.to_py_mat(obj)
    def to_row_vec(self, obj):
        return TiCollections.to_py_row_vec(obj)
    def to_col_vec(self, obj):
        return TiCollections.to_py_col_vec(obj)        




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
        if not  py_mat_str.endswith("]]"):
            return False
        if ", " in py_mat_str:
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
        elif TiCollections.is_ti_list(ti_list_str):
            return [convert_element(x.strip()) for x in ti_list_str[1:-1].split(",")]
        elif TiCollections.is_py_list_str(ti_list_str):
            return TiCollections.py_str_to_list(ti_list_str)
        raise UnconvertableString("Cannot convert to list: {}".format(ti_list_str))

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
    def to_ti_row_vec(matrix: list) -> str:
        if TiCollections.is_ti_row_vec(matrix):
            return matrix
        return TiCollections.to_ti_mat(TiCollections.to_py_row_vec(matrix))
    
    
    @staticmethod
    def flatten(lst: list) -> list:
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
