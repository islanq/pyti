import sys
from ti_expression import TiExpression   
from ti_collections import TiCollections

if sys.platform == 'TI-Nspire':
    
    #from eval_expr import eval_expr, call_func
    pass
else:
    pass
    #call_func = TiCollections.call_func
    #eval_expr = TiCollections.eval_expr
from ti_interop import tiexec





class TiMatrix(TiCollections):
    
    def __init__(self, matrix_or_str: (str, list) = None):
        if not matrix_or_str:
            matrix_or_str = [[]]
        self.ti_matrix = self.to_ti_mat(matrix_or_str)
        self.py_matrix = self.to_py_mat(self.ti_matrix)
        self.data = self.py_matrix
        self.rows = len(self.data)
        self.cols = len(self.data[0]) if self.py_matrix else 0
        self._current_row = 0
        self._current_col = 0
       
    
    # @property
    # def cols(self) -> int:
    #     return int(self.col_dim(self.ti_matrix))
    
    # @property
    # def rows(self) -> int:
    #     return int(self.row_dim(self.ti_matrix))
    
    @property
    def T(self) -> 'TiMatrix':
        return self.transpose()
    
    def __PyMatrix__(self):
        return self.py_matrix
    
    def __list__(self):
        return self.py_matrix
    
    def __PyList__(self):
        return self.py_matrix
    
    def __getitem__(self, indices):
        return self.data[indices[0]][indices[1]] if isinstance(indices, tuple) else self.data[indices]
    
    def __setitem__(self, indices, value):
        if isinstance(indices, tuple):
            row, col = indices
            self.data[row][col] = value
        else:
            self.data[indices] = value
    
    def __iter__(self):
        self._current_row, self._current_col = 0, 0
        return self

    def __next__(self):
        # If we've reached the end of the matrix, raise StopIteration
        if self._current_row == self.rows:
            raise StopIteration

        # Get the current item in the matrix
        item = self.data[self._current_row]

        # Update the current row and column indices for the next iteration
        self._current_row += 1

        return item
    
    
    
    def exact(self) -> 'TiMatrix':
        return TiMatrix(tiexec("exact", self.ti_matrix))
        return TiMatrix(call_func("exact", self.ti_matrix))
    
    def abs(self) -> 'TiMatrix':
        return TiMatrix(tiexec("abs", self.ti_matrix))
        return TiMatrix(call_func("abs", self.ti_matrix))
    
    def expand(self, var = None) -> 'TiMatrix':
        return TiMatrix(tiexec("expand", self.ti_matrix))
    
    def factor(self, var = None) -> 'TiMatrix':
        return TiMatrix(tiexec("factor", self.ti_matrix))
    
    def augment(self, matrix) -> 'TiMatrix':
        """
            Returns a new matrix that is Matrix2
            appended to Matrix1. When the “,”
            character is used, the matrices must have
            equal row dimensions, and Matrix2 is
            appended to Matrix1 as new columns.
            Does not alter Matrix1 or Matrix2.
        """
        if TiCollections.is_py_mat(matrix):
            matrix = TiCollections.to_ti_mat(matrix)
        return TiMatrix(tiexec("augment", self.ti_matrix + "," + matrix))
        return TiMatrix(call_func("augment", self.ti_matrix + "," + matrix))

    def col_augment(self, matrix) -> 'TiMatrix':
        """
            Returns a new py_matrix1 that is `py_matrix2
            appended to py_matrix1`. The matrices must
            have equal column dimensions, and
            `py_matrix2 is appended to py_matrix1 as new
            rows`. Does not alter py_matrix1 or py_matrix2
        """

    
        if TiCollections.is_py_mat(matrix):
            matrix = TiCollections.to_ti_mat(matrix)
        return TiMatrix(tiexec("colAugment", self.ti_matrix, matrix))
        return TiMatrix(call_func("colAugment", self.ti_matrix, matrix))

            
    def conj(self) -> 'TiMatrix':
        """
            Returns the complex conjugate of the argument.
        """
        return TiMatrix(tiexec("conj", self.ti_matrix))


    def gcd(self, matrix) -> 'TiMatrix':
        """
            Returns the greatest common divisor of the
            elements in the matrix.
        """
        if TiCollections.is_py_mat(matrix):
            matrix = TiCollections.to_ti_mat(matrix)
        return TiMatrix(tiexec("gcd", self.ti_matrix, matrix))
        return TiMatrix(call_func("gcd", self.ti_matrix + "," + matrix))

    def lcm(self, matrix) -> 'TiMatrix':
        """
            Returns the least common multiple of the
            elements in the matrix.
        """
        if TiCollections.is_py_mat(matrix):
            matrix = TiCollections.to_ti_mat(matrix)
        return TiMatrix(tiexec("lcm", self.ti_matrix, matrix))

    def sub_mat(self, start_row=None, start_col=None, end_row=None, end_col=None) -> 'TiMatrix':
        """
            Returns the specified submatrix.
            Defaults: start_row=1, start_col=1,
            end_row=last row, end_col=last column
        """
        args = [str(arg) for arg in [start_row, start_col, end_row, end_col] if arg is not None]
        return TiMatrix(tiexec("subMat", self.ti_matrix + "," + ",".join(args)))
        return TiMatrix(call_func("subMat", self.ti_matrix + "," + ",".join(args)))

    @staticmethod
    def construct_mat(expr, var1: str, var2:str, num_rows: int, num_cols:int) -> 'TiMatrix':
        
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
        return TiMatrix(tiexec("constructMat", expr, var1, var2, num_rows, num_cols))
        return TiMatrix(call_func("constructMat", expr, var1, var2, num_rows, num_cols))
    
    @staticmethod
    def rand_mat(num_rows: int, num_cols: int) -> 'TiMatrix': # working
        return TiMatrix(tiexec("randMat", num_rows, num_cols))  
        return TiMatrix(call_func("randMat", num_rows, num_cols))  

    def comulative_sum(self) -> 'TiMatrix':
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
        return TiMatrix(tiexec("cumulativeSum", self.ti_matrix))
        return TiMatrix(call_func("cumulativeSum", self.ti_matrix))
       
    def com_denom(self) -> TiExpression:
        """
            Returns the maximum of the sums of the
            absolute values of the elements in the
            columns in Matrix.
        """
        return TiMatrix(tiexec("comDenom", self.ti_matrix))
    
    def eig_vc(self) -> 'TiMatrix':
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
        #return TiMatrix(call_func("abs", self.ti_matrix))
        return TiMatrix(tiexec("abs", self.ti_matrix))

    def min(self, matrix: ('TiMatrix', list) = None) -> 'TiMatrix':
        """
            With no parameters, returns a row vector containing
            the minimum element of each column in Matrix1.
            
            if `matrix` is passed, it
            returns the minimum of the two
            arguments. If the arguments are two lists
            or matrices, returns a list or matrix
            containing the minimum value of each pair
            of corresponding elements.
        """
        if matrix and TiCollections.is_py_mat(matrix):
            matrix = TiCollections.to_ti_mat(matrix)
            return TiMatrix(tiexec("min", self.ti_matrix, matrix))
        elif matrix and TiCollections.is_ti_mat(matrix):
            return TiMatrix(tiexec("min", self.ti_matrix, matrix))
        else:
            return TiMatrix(tiexec("min", self.ti_matrix))

    def max(self, matrix: ('TiMatrix', list) = None) -> 'TiMatrix':
        """
            With no parameters, returns a row vector containing
            the maximum element of each column in Matrix1.
            
            if `matrix` is passed, it
            returns the maximum of the two
            arguments. If the arguments are two lists
            or matrices, returns a list or matrix
            containing the maximum value of each pair
            of corresponding elements.
        """
        if matrix and TiCollections.is_py_mat(matrix):
            matrix = TiCollections.to_ti_mat(matrix)
        return TiMatrix(tiexec("max", self.ti_matrix, matrix))
    
    
    def median(self, matrix = None) -> 'TiMatrix':
        """
            Returns a row vector containing the
            medians of the columns in Matrix1.
            Each freqMatrix element counts the
            number of consecutive occurrences of the
            corresponding element in Matrix1
        """
        if matrix and TiCollections.is_py_mat(matrix):
            matrix = TiCollections.to_ti_mat(matrix)
            return TiMatrix(tiexec("median", self.ti_matrix, matrix))
        elif matrix and TiCollections.is_ti_mat(matrix):
            return TiMatrix(tiexec("median", self.ti_matrix, matrix))
        else:
            return TiMatrix(tiexec("median", self.ti_matrix))
        
        
    
    def eig_vl(self) -> 'TiMatrix':
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
        #return TiMatrix(call_func("eigVl", self.ti_matrix))
        return TiMatrix(tiexec("eigVl", self.ti_matrix))
    
    def floor(self) -> 'TiMatrix':
        #return TiMatrix(call_func("floor", self.ti_matrix))
        return TiMatrix(tiexec("floor", self.ti_matrix))
    
    def det(self, tol=None) -> TiExpression:
        if tol is not None:
            return TiMatrix(tiexec("det", self.ti_matrix + "," + str(tol)))
            return TiMatrix(call_func("det", self.ti_matrix + "," + str(tol)))
        else:
            return TiMatrix(tiexec("det", self.ti_matrix))
            return TiMatrix(call_func("det", self.ti_matrix))

    def diag(self) -> 'TiMatrix':
        return TiMatrix(tiexec("diag", self.ti_matrix))
        return TiMatrix(call_func("diag", self.ti_matrix))
    
    def row_add(self, sum_with_row, sum_to_row) -> 'TiMatrix':
        """
            Returns a copy of matrix with row
            sum_to_row replaced by the sum of rows
            sum_with_row and sum_to_row.
        """
        return TiMatrix(tiexec("rowAdd", self.ti_matrix + "," + str(sum_with_row) + "," + str(sum_to_row)))
        return TiMatrix(call_func("rowAdd", self.ti_matrix + "," + str(sum_with_row) + "," + str(sum_to_row)))
    
    def imag(self) -> 'TiMatrix':
        return TiMatrix(tiexec("imag", self.ti_matrix))
    
    
    def int(self) -> 'TiMatrix':
        return TiMatrix(tiexec("int", self.ti_matrix))
    
    def int_div(self, matrix) -> 'TiMatrix':
        if TiCollections.is_py_mat(matrix):
            matrix = TiMatrix(matrix)
        return TiMatrix(tiexec("intDiv", self.ti_matrix, matrix))
    
    # TODO fix
    def row_sub(self, input_matrix, row_to_subtract: int, row_to_target: int, factor=1):

        row_subtract_values = self.get_row(self.ti_matrix, row_to_subtract)
        row_subtract_target = self.get_row(self.ti_matrix, row_to_target)
        
        sub_matrix = TiCollections.to_ti_mat(row_subtract_values)
        tar_matrix = TiCollections.to_ti_mat(row_subtract_target)
        
        subtracted_result_str = self.tiexec("{}-{}*{}".format(tar_matrix, sub_matrix, factor))
        subtracted_result_vec = TiCollections.to_py_mat(subtracted_result_str)[0]
        
        result_py_matrix = [row for row in input_matrix]
        result_py_matrix[row_to_target - 1] = subtracted_result_vec
        
        return result_py_matrix

    def m_row(self, expr, row_idx) -> 'TiMatrix':
        """
            Returns a copy of the matrix with each
            element in row row_idx multiplied
            by `expr`.
        
        """
        return TiMatrix(tiexec("mRow", str(expr) + "," + self.ti_matrix + "," + str(row_idx)))
        return TiMatrix(call_func("mRow", str(expr) + "," + self.ti_matrix + "," + str(row_idx)))

    def m_row_add(self, expr, mulexpr_row, update_row_idx) -> 'TiMatrix':
        """
            Returns a copy of the matrix with each
            element in row the update_row of replaced
            with:
            expr • mulexpr_row + update_row_idx
        """
        #result_str = call_func("mRowAdd", str(expr) + "," + self.ti_matrix + "," + str(mulexpr_row) + "," + str(update_row_idx))
        result_str = tiexec("mRowAdd", str(expr) + "," + self.ti_matrix + "," + str(mulexpr_row) + "," + str(update_row_idx))
        return TiMatrix(result_str)
    
    @staticmethod
    def identity(self, size: int) -> 'TiMatrix':
        return TiMatrix(tiexec("identity", size))
        return TiMatrix(call_func("identity", size))

    def col_norm(self) -> TiExpression:
        #return TiMatrix(call_func("colNorm", self.ti_matrix))
        return TiMatrix(tiexec("colNorm", self.ti_matrix))
    
    def row_norm(self) -> TiExpression:
        #return TiMatrix(call_func("rowNorm", self.ti_matrix))
        return TiMatrix(tiexec("rowNorm", self.ti_matrix))

    def col_dim(self, ti_force = False) -> TiExpression:
        if not ti_force:
            return len(self.py_matrix[0])
        #return TiMatrix(call_func("colDim", self.ti_matrix))
        return tiexec("colDim", self.ti_matrix)

    def row_dim(self, ti_force = False) -> TiExpression:
        return tiexec("rowDim", self.ti_matrix)
        return TiExpression(call_func("rowDim", self.ti_matrix))

    def row_swap(self, row1, row2, ti_force = False) -> 'TiMatrix':
        #return TiMatrix(call_func("rowSwap", self.ti_matrix, row1, row2))
        return TiMatrix(tiexec("rowSwap", self.ti_matrix, row1, row2))
    
    def get_row(self, row_idx) -> 'TiMatrix': 
        return TiMatrix(self.tiexec("{}[{}]".format(self.ti_matrix, row_idx)))

    def get_col(self, col_idx):
        args = (self.ti_matrix, 1, col_idx, self.col_dim, col_idx)
        return TiMatrix(self.tiexec("subMat", *args))

    def ref(self):
        #TiMatrix(call_func("ref", self.ti_matrix))
        TiMatrix(tiexec("ref", self.ti_matrix))

    def rref(self, tol=None) -> 'TiMatrix':
        if tol is not None:
            return TiMatrix(tiexec("rref", self.ti_matrix + "," + str(tol)))
            return TiMatrix(call_func("rref", self.ti_matrix + "," + str(tol)))
        else:
            return TiMatrix(tiexec("rref", self.ti_matrix))
            return TiMatrix(call_func("rref", self.ti_matrix))

    # TODO fix
    def simult(self, py_coeff_matrix, const_col_vector, tol=None):
        ti_coeff_matrix = TiCollections.to_ti_mat(py_coeff_matrix)
        ti_const_vector = TiCollections.to_ti_mat(const_col_vector)
        if tol is not None:
            result_str = tiexec("simult", ti_coeff_matrix + "," + ti_const_vector + "," + str(tol))
            #result_str = call_func("simult", ti_coeff_matrix + "," + ti_const_vector + "," + str(tol))
        else:
            result_str = tiexec("simult", ti_coeff_matrix + "," + ti_const_vector)
        return TiMatrix(result_str)

    def ipart(self)-> 'TiMatrix':
        return TiMatrix(tiexec("ipart", self.ti_matrix))

    def transpose(self) -> 'TiMatrix':
        return TiMatrix(tiexec("{}@t".format(self.ti_matrix)))
    
    def inverse(self) -> 'TiMatrix':
        #return TiMatrix(eval_expr("({}^-1)".format(self.ti_matrix)))
        return TiMatrix(tiexec("({}^-1)".format(self.ti_matrix)))
    
    def __repr__(self):
        return self.ti_matrix
    
    def __str__(self):
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