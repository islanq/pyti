import sys
if sys.platform == 'win32':
    exec(open('__init__.py').read())
if sys.platform == 'TI-Nspire':
    from eval_expr import eval_expr, call_func
else:
    call_func = TiCollections.call_func
    eval_expr = TiCollections.eval_expr
    
from ti_collections import TiCollections
    
class TiMatrix(TiCollections):
    
    def __init__(self, matrix_or_str: (str, list) = None):
        if not matrix_or_str:
            matrix_or_str = [[]]
        self.ti_matrix = self.to_ti_mat(matrix_or_str)
        self.py_matrix = self.to_py_mat(self.ti_matrix)
       
    
    def abs(self, py_matrix):
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("abs", ti_matrix)
        return TiCollections.to_py_mat(result_str)
    
    def augment(self, py_matrix1, py_matrix2):
        ti_matrix1 = TiCollections.to_ti_mat(py_matrix1)
        ti_matrix2 = TiCollections.to_ti_mat(py_matrix2)
        result_str = call_func("augment", ti_matrix1 + "," + ti_matrix2)
        return TiCollections.to_py_mat(result_str)

    def col_augment(self, py_matrix1, py_matrix2):
        """
            Returns a new py_matrix1 that is `py_matrix2
            appended to py_matrix1`. The matrices must
            have equal column dimensions, and
            `py_matrix2 is appended to py_matrix1 as new
            rows`. Does not alter py_matrix1 or py_matrix2
        """
        ti_matrix1 = TiCollections.to_ti_mat(py_matrix1)
        ti_matrix2 = TiCollections.to_ti_mat(py_matrix2)
        result_str = call_func("colAugment", ti_matrix1, ti_matrix2)
        return TiCollections.to_py_mat(result_str)

    def sub_mat(self, py_matrix, start_row=None, start_col=None, end_row=None, end_col=None):
        """
            Returns the specified submatrix.
            Defaults: start_row=1, start_col=1,
            end_row=last row, end_col=last column
        """
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        args = [str(arg) for arg in [start_row, start_col, end_row, end_col] if arg is not None]
        result_str = call_func("subMat", ti_matrix + "," + ",".join(args))
        return TiCollections.to_py_mat(result_str)

    def construct_mat(expr, var1: str, var2:str, num_rows: int, num_cols:int):
        
        """
            expr is an expression in variables var1 and
            var2. Elements in the resulting matrix are
            formed by evaluating expr for each
            incremented value of var1 and var2.
            
            var1 is automatically incremented from `1`
            through num_rows.
            
            Within each row, var2
            is incremented from `1` through num_cols.        
        """
        result_str = call_func("constructMat", expr, var1, var2, num_rows, num_cols)
        return TiCollections.to_py_mat(result_str)
    
    def rand_mat(self, num_rows: int, num_cols: int): # working
        result_str = call_func("randMat", num_rows, num_cols)
        return TiCollections.to_py_mat(result_str)    

    def comulative_sum(self, py_matrix):
        """
            cumulativeSum(py_matrix) ⇒ matrix
            Returns a matrix of the cumulative sums of
            the elements in py_matrix. Each element is
            the cumulative sum of the column from top
            to bottom.
            An empty (void) element in List1 or
            py_matrix produces a void element in the
            resulting list or matrix. For more
            information on empty elements, see page
        """
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("cumulativeSum", ti_matrix)
        return TiCollections.to_py_mat(result_str)
    
    def eig_vc(self, py_matrix):
        """
            eigVc(squareMatrix) ⇒ matrix
            Returns a matrix containing the
            eigenvectors for a real or complex
            squareMatrix, where each column in the
            result corresponds to an eigenvalue. Note
            that an eigenvector is not unique; it may be
            scaled by any constant factor. The
            eigenvectors are normalized, meaning that:
            if V = [x_1, x_2, … , x_n]
            then x_1^2 + x_2^2 + … + x_n^2 = 1
        """
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("eigVc", ti_matrix)
        return TiCollections.to_py_mat(result_str)
        
    def eig_vl(self, py_matrix):
        """
            eigVc(squareMatrix) ⇒ matrix
            Returns a matrix containing the
            eigenvectors for a real or complex
            squareMatrix, where each column in the
            result corresponds to an eigenvalue. Note
            that an eigenvector is not unique; it may be
            scaled by any constant factor. The
            eigenvectors are normalized, meaning that:
            if V = [x_1, x_2, … , x_n]
            then x_1^2 + x_2^2 + … + x_n^2 = 1
        """
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("eigVl", ti_matrix)
        return TiCollections.to_py_mat(result_str)    
    
    def floor(self):
        
        #ti_matrix = TiCollections.to_ti_mat(py_matrix)
        return TiMatrix(call_func("floor", self.ti_matrix))
        return TiCollections.to_py_mat(result_str)
    
    def det(self, py_matrix, tol=None):
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        if tol is not None:
            result_str = call_func("det", ti_matrix + "," + str(tol))
        else:
            result_str = call_func("det", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    def diag(self, py_list_or_matrix):
        if isinstance(py_list_or_matrix[0], list):  # Assuming it's a matrix
            ti_matrix = TiCollections.to_ti_mat(py_list_or_matrix)
            result_str = call_func("diag", ti_matrix)
        else:  # Assuming it's a list
            ti_list = TiCollections.to_ti_list(py_list_or_matrix)
            result_str = call_func("diag", ti_list)
        return TiCollections.to_py_mat(result_str)
    
    def row_add(self, py_matrix, sum_with_row, sum_to_row):
        """
            Returns a copy of matrix with row
            sum_to_row replaced by the sum of rows
            sum_with_row and sum_to_row.

        """
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("rowAdd", ti_matrix + "," + str(sum_with_row) + "," + str(sum_to_row))
        return TiCollections.to_py_mat(result_str)
    
    def row_sub(self, input_matrix, row_to_subtract, row_to_target, factor=1):

        row_subtract_values = self.get_row(input_matrix, row_to_subtract)
        row_subtract_target = self.get_row(input_matrix, row_to_target)
        
        sub_matrix = TiCollections.to_ti_mat(row_subtract_values)
        tar_matrix = TiCollections.to_ti_mat(row_subtract_target)
        
        subtracted_result_str = self.tiexec("{}-{}*{}".format(tar_matrix, sub_matrix, factor))
        subtracted_result_vec = TiCollections.to_py_mat(subtracted_result_str)[0]
        
        result_py_matrix = [row for row in input_matrix]
        result_py_matrix[row_to_target - 1] = subtracted_result_vec
        
        return result_py_matrix

    def m_row(self, expr, matrix, row_idx):
        """
            Returns a copy of the matrix with each
            element in row row_idx multiplied
            by `expr`.
        
        """
        ti_matrix = TiCollections.to_ti_mat(matrix)
        result_str = call_func("mRow", str(expr) + "," + ti_matrix + "," + str(row_idx))
        return TiCollections.to_py_mat(result_str)

    def m_row_add(self, expr, matrix, mulexpr_row, update_row_idx):
        """
            Returns a copy of the matrix with each
            element in row the update_row of replaced
            with:
            expr • mulexpr_row + update_row_idx
        """
        ti_matrix = TiCollections.to_ti_mat(matrix)
        result_str = call_func("mRowAdd", str(expr) + "," + ti_matrix + "," + str(mulexpr_row) + "," + str(update_row_idx))
        return TiCollections.to_py_mat(result_str)
    
    def identity(self, size: int):
        result_str = call_func("identity", size)
        return TiCollections.to_py_mat(result_str)

    def col_norm(self, py_matrix):
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("colNorm", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression
    
    def row_norm(self, py_matrix):
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("rowNorm", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    def col_dim(self, py_matrix, ti_force = False):
        if not ti_force:
            return len(py_matrix[0])
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("colDim", ti_matrix)
        return int(result_str)  # Assuming it returns a scalar value or expression   

    def row_dim(self, py_matrix, ti_force = False):
        if not ti_force:
            return len(py_matrix)
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("rowDim", ti_matrix)
        return int(result_str)  # Assuming it returns a scalar value or expression

    def row_swap(self, py_matrix, row1, row2, ti_force = False):
        if not ti_force:
            matrix = [row for row in py_matrix]
            matrix[row1 - 1], matrix[row2 - 1] = matrix[row2 - 1], matrix[row1 - 1]
            return matrix
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("rowSwap", ti_matrix + "," + str(row1) + "," + str(row2))
        result_str = call_func("rowSwap", ti_matrix, row1, row2)
        return TiCollections.to_py_mat(result_str)
    
    def get_row(self, py_matrix, row_idx): 
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = self.tiexec("{}[{}]".format(ti_matrix, row_idx))
        return TiCollections.to_py_mat(result_str)

    def get_col(self, py_matrix, col_idx):
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        max_row = len(py_matrix)
        args = (ti_matrix, 1, col_idx, max_row, col_idx)
        result_str = self.tiexec("subMat", *args)
        return TiCollections.to_py_mat(result_str)

    def ref(self, py_matrix):
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = call_func("ref", ti_matrix)
        return TiCollections.to_py_mat(result_str)

    def rref(self, py_matrix, tol=None):
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        if tol is not None:
            result_str = call_func("rref", ti_matrix + "," + str(tol))
        else:
            result_str = call_func("rref", ti_matrix)
        return TiCollections.to_py_mat(result_str)

    def simult(self, py_coeff_matrix, const_col_vector, tol=None):
        ti_coeff_matrix = TiCollections.to_ti_mat(py_coeff_matrix)
        ti_const_vector = TiCollections.to_ti_mat(const_col_vector)
        if tol is not None:
            result_str = call_func("simult", ti_coeff_matrix + "," + ti_const_vector + "," + str(tol))
        else:
            result_str = call_func("simult", ti_coeff_matrix + "," + ti_const_vector)
        return TiCollections.to_py_mat(result_str)

    def transpose(self, py_matrix):
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = eval_expr("{}@t".format(ti_matrix))
        return TiCollections.to_py_mat(result_str)
    
    def inverse(self, py_matrix):
        ti_matrix = TiCollections.to_ti_mat(py_matrix)
        result_str = eval_expr("({}^-1)".format(ti_matrix))
        return TiCollections.to_py_mat(result_str)
    
    def __repr__(self):
        return self.ti_matrix
    
    """
    
    
    def log_matrix_operation(operation):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if operation == "swap":
                print(f"r{args[1]} <-> r{args[2]}")
            elif operation == "multiply":
                print(f"r{args[1]} <- r{args[1]} * {args[2]}")
            elif operation == "add":
                print(f"r{args[1]} <- r{args[1]} + r{args[2]}")
            elif operation == "m_row_add":
                print(f"r{args[1]} <- r{args[1]} + {args[2]} * r{args[3]}")
            elif operation == "sub":
                print(f"r{args[1]} <- r{args[1]} - r{args[2]}")
            elif operation == "div":
                print(f"r{args[1]} <- r{args[1]} / {args[2]}")
            # Add more operation types if needed
            
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

# Usage

@log_matrix_operation("swap")
def swap_rows(matrix, row1, row2):
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
    return matrix

@log_matrix_operation("multiply")
def multiply_row(matrix, row, scalar):
    matrix[row] = [x * scalar for x in matrix[row]]
    return matrix

@log_matrix_operation("add")
def add_rows(matrix, target_row, source_row):
    matrix[target_row] = [x + y for x, y in zip(matrix[target_row], matrix[source_row])]
    return matrix

@log_matrix_operation("m_row_add")
def m_row_add(matrix, target_row, scalar, source_row):
    matrix[target_row] = [x + scalar * y for x, y in zip(matrix[target_row], matrix[source_row])]
    return matrix

@log_matrix_operation("sub")
def sub_rows(matrix, target_row, source_row):
    matrix[target_row] = [x - y for x, y in zip(matrix[target_row], matrix[source_row])]
    return matrix

@log_matrix_operation("div")
def div_row(matrix, row, scalar):
    matrix[row] = [x / scalar for x in matrix[row]]
    return matrix

# Test
mat = [[1, 2], [3, 4]]

swap_rows(mat, 0, 1)
multiply_row(mat, 0, 2)
add_rows(mat, 0, 1)
m_row_add(mat, 0, 2, 1)
sub_rows(mat, 0, 1)
div_row(mat, 0, 2)

    
    
    
    
    
    
    
    
    
    """
    
    
    
    """
    
    
    
    def deduce_matrix_operation(initial_matrix, final_matrix):
    if len(initial_matrix) != len(final_matrix):
        return "The number of rows has changed. Cannot deduce operation."
    if len(initial_matrix[0]) != len(final_matrix[0]):
        return "The number of columns has changed. Cannot deduce operation."
    
    changed_row = None
    changed_count = 0
    
    for i in range(len(initial_matrix)):
        if initial_matrix[i] != final_matrix[i]:
            changed_row = i
            changed_count += 1
            
    if changed_count == 0:
        return "No operation detected."
    
    if changed_count > 1:
        return "Multiple rows have changed. Cannot deduce operation."
    
    initial_row = initial_matrix[changed_row]
    final_row = final_matrix[changed_row]
    
    # Check for scalar multiplication
    scalar = final_row[0] / initial_row[0] if initial_row[0] != 0 else None
    if all(fr == ir * scalar for fr, ir in zip(final_row, initial_row)):
        return f"Row {changed_row + 1} was multiplied by {scalar}."
    
    # Check for row addition
    diff = [fr - ir for fr, ir in zip(final_row, initial_row)]
    for i in range(len(initial_matrix)):
        if i == changed_row:
            continue
        if all(d == ir for d, ir in zip(diff, initial_matrix[i])):
            return f"Row {changed_row + 1} was replaced by the sum of row {changed_row + 1} and row {i + 1}."
    
    return "Could not deduce operation."

    
    
    
    
    """