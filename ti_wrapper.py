import sys
if sys.platform == 'TI-Nspire':
    from inter import Interoperability
    from eval_expr import eval_expr, call_func
else:
    from ti_interop import Interop
    
class TiWrapper(Interop):
    
    def augment(self, py_matrix1, py_matrix2): # working
        ti_matrix1 = Interop.to_ti_mat(py_matrix1)
        ti_matrix2 = Interop.to_ti_mat(py_matrix2)
        result_str = call_func("augment", ti_matrix1 + "," + ti_matrix2)
        return Interop.to_py_mat(result_str)

    def col_augment(self, py_matrix1, py_matrix2): # working
        """
            Returns a new py_matrix1 that is `py_matrix2
            appended to py_matrix1`. The matrices must
            have equal column dimensions, and
            `py_matrix2 is appended to py_matrix1 as new
            rows`. Does not alter py_matrix1 or py_matrix2
            
            
        """
        ti_matrix1 = Interop.to_ti_mat(py_matrix1)
        ti_matrix2 = Interop.to_ti_mat(py_matrix2)
        result_str = call_func("colAugment", ti_matrix1, ti_matrix2)
        return result_str  # Assuming it returns a scalar value or expression

    def sub_mat(self, py_matrix, start_row=None, start_col=None, end_row=None, end_col=None): # working
        """
            Returns the specified submatrix.
            Defaults: start_row=1, start_col=1,
            end_row=last row, end_col=last column
        """
        ti_matrix = Interop.to_ti_mat(py_matrix)
        args = [str(arg) for arg in [start_row, start_col, end_row, end_col] if arg is not None]
        result_str = call_func("subMat", ti_matrix + "," + ",".join(args))
        return Interop.to_py_mat(result_str)


    def construct_mat(expr, var1, var2, num_rows, num_cols):
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
        raise NotImplementedError
        pass
    
    def rand_mat(self, num_rows: int, num_cols: int): # working
        result_str = call_func("randMat", num_rows, num_cols)
        return Interop.to_py_mat(result_str)    

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
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = call_func("cumulativeSum", ti_matrix)
        return Interop.to_py_mat(result_str)
    
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
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = call_func("eigVc", ti_matrix)
        return Interop.to_py_mat(result_str)
        
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
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = call_func("eigVl", ti_matrix)
        return Interop.to_py_mat(result_str)    
    
    
    def det(self, py_matrix, tol=None): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        if tol is not None:
            result_str = call_func("det", ti_matrix + "," + str(tol))
        else:
            result_str = call_func("det", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    def diag(self, py_list_or_matrix):
        if isinstance(py_list_or_matrix[0], list):  # Assuming it's a matrix
            ti_matrix = Interop.to_ti_mat(py_list_or_matrix)
            result_str = call_func("diag", ti_matrix)
        else:  # Assuming it's a list
            ti_list = Interop.to_ti_list(py_list_or_matrix)
            result_str = call_func("diag", ti_list)
        return Interop.to_py_mat(result_str)
    
    def row_add(self, py_matrix, sum_with_row, sum_to_row): # working
        """
            Returns a copy of matrix with row
            sum_to_row replaced by the sum of rows
            sum_with_row and sum_to_row.

        """
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = call_func("rowAdd", ti_matrix + "," + str(sum_with_row) + "," + str(sum_to_row))
        return Interop.to_py_mat(result_str)

    def m_row(self, expr, matrix, row_idx): # working
        """
            Returns a copy of the matrix with each
            element in row row_idx multiplied
            by `expr`.
        
        """
        ti_matrix = Interop.to_ti_mat(matrix)
        result_str = call_func("mRow", str(expr) + "," + ti_matrix + "," + str(row_idx))
        return Interop.to_py_mat(result_str)

    def m_row_add(self, expr, matrix, mulexpr_row, update_row_idx): # working
        """
            Returns a copy of the matrix with each
            element in row the update_row of replaced
            with:
            expr • mulexpr_row + update_row_idx
        """
        ti_matrix = Interop.to_ti_mat(matrix)
        result_str = call_func("mRowAdd", str(expr) + "," + ti_matrix + "," + str(mulexpr_row) + "," + str(update_row_idx))
        return Interop.to_py_mat(result_str)
   
   
       
       
    
    def identity(self, size: int): # working
        """
        """
        result_str = call_func("identity", size)
        return Interop.to_py_mat(result_str)

    def col_norm(self, py_matrix): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = call_func("colNorm", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression
    
    def row_norm(self, py_matrix): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = call_func("rowNorm", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    def col_dim(self, py_matrix): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = call_func("colDim", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    def row_dim(self, py_matrix): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = call_func("rowDim", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    def row_swap(self, py_matrix, row1, row2): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        #result_str = call_func("rowSwap", ti_matrix + "," + str(row1) + "," + str(row2))
        result_str = call_func("rowSwap", ti_matrix, row1, row2)
        return Interop.to_py_mat(result_str)


    def ref(self, py_matrix): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = call_func("ref", ti_matrix)
        return Interop.to_py_mat(result_str)

    def rref(self, py_matrix, tol=None): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        if tol is not None:
            result_str = call_func("rref", ti_matrix + "," + str(tol))
        else:
            result_str = call_func("rref", ti_matrix)
        return Interop.to_py_mat(result_str)

    def simult(self, py_coeff_matrix, const_col_vector, tol=None):
        ti_coeff_matrix = Interop.to_ti_mat(py_coeff_matrix)
        ti_const_vector = Interop.to_ti_mat(const_col_vector)
        if tol is not None:
            result_str = call_func("simult", ti_coeff_matrix + "," + ti_const_vector + "," + str(tol))
        else:
            result_str = call_func("simult", ti_coeff_matrix + "," + ti_const_vector)
        return Interop.to_py_mat(result_str)

    def transpose(self, py_matrix): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = eval_expr("{}@t".format(ti_matrix))
        return Interop.to_py_mat(result_str)
    
    def inverse(self, py_matrix): # working
        ti_matrix = Interop.to_ti_mat(py_matrix)
        result_str = eval_expr("({}^-1)".format(ti_matrix))
        return Interop.to_py_mat(result_str)