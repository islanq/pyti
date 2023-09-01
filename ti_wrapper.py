import sys
if sys.platform == 'TI-Nspire':
    from inter import Interoperability
    from eval_expr import eval_expr, call_func
else:
    from ti_interop import Interoperability


class TiWrapper(Interoperability):
    
    def augment(self, py_matrix1, py_matrix2):
        ti_matrix1 = Interoperability.to_ti_mat(py_matrix1)
        ti_matrix2 = Interoperability.to_ti_mat(py_matrix2)
        result_str = call_func("augment", ti_matrix1 + "," + ti_matrix2)
        return Interoperability.to_py_mat(result_str)

    def col_augment(self, py_matrix1, py_matrix2):
        """
            Returns a new matrix that is `matrix2
            appended to matrix1`. The matrices must
            have equal column dimensions, and
            `matrix2 is appended to matrix1 as new
            rows`. Does not alter matrix1 or matrix2
        """
        ti_matrix1 = Interoperability.to_ti_mat(py_matrix1)
        ti_matrix2 = Interoperability.to_ti_mat(py_matrix2)
        result_str = call_func("colDim", ti_matrix1, ti_matrix2)
        return result_str  # Assuming it returns a scalar value or expression

    def construct_mat(expr, var1, var2, num_rows, num_cols):
        """
            Expr is an expression in variables var1 and
            var2. Elements in the resulting matrix are
            formed by evaluating Expr for each
            incremented value of var1 and var2.
            
            var1 is automatically incremented from `1`
            through num_rows.
            
            Within each row, Var2
            is incremented from `1` through num_cols.        
        """
        raise NotImplementedError
        pass
    
    # tested
    def det(self, py_matrix, tol=None):
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        if tol is not None:
            result_str = call_func("det", ti_matrix + "," + str(tol))
        else:
            result_str = call_func("det", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    def diag(self, py_list_or_matrix):
        if isinstance(py_list_or_matrix[0], list):  # Assuming it's a matrix
            ti_matrix = Interoperability.to_ti_mat(py_list_or_matrix)
            result_str = call_func("diag", ti_matrix)
        else:  # Assuming it's a list
            ti_list = Interoperability.to_ti_list(py_list_or_matrix)
            result_str = call_func("diag", ti_list)
        return Interoperability.to_py_mat(result_str)

    def sub_mat(self, py_matrix, start_row=None, start_col=None, end_row=None, end_col=None):
        """
            Returns the specified submatrix.
            Defaults: start_row=1, start_col=1,
            end_row=last row, end_col=last column
        """
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        args = [str(arg) for arg in [start_row, start_col, end_row, end_col] if arg is not None]
        result_str = call_func("subMat", ti_matrix + "," + ",".join(args))
        return Interoperability.to_py_mat(result_str)
    
    # tested
    def row_add(self, py_matrix, sum_with_row, sum_to_row):
        """
            Returns a copy of matrix with row
            rIndex2 replaced by the sum of rows
            rIndex1 and rIndex2.

        """
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        result_str = call_func("rowAdd", ti_matrix + "," + str(sum_with_row) + "," + str(sum_to_row))
        return Interoperability.to_py_mat(result_str)

    # tested
    def m_row(self, expr, matrix, row_idx):
        """
            Returns a copy of the matrix with each
            element in row row_idx multiplied
            by `expr`.
        
        """
        ti_matrix = Interoperability.to_ti_mat(matrix)
        result_str = call_func("mRow", str(expr) + "," + ti_matrix + "," + str(row_idx))
        return Interoperability.to_py_mat(result_str)

    # tested
    def m_row_add(self, expr, matrix, mulexpr_row, update_row_idx):
        """
            Returns a copy of the matrix with each
            element in row the update_row of replaced
            with:
            expr • row Index1 + row Index2
        """
        ti_matrix = Interoperability.to_ti_mat(matrix)
        result_str = call_func("mRowAdd", str(expr) + "," + ti_matrix + "," + str(mulexpr_row) + "," + str(update_row_idx))
        return Interoperability.to_py_mat(result_str)
   
    #tested
    def rand_mat(self, num_rows, num_cols):
        result_str = call_func("randMat", str(num_rows) , str(num_cols))
        return Interoperability.to_py_mat(result_str)
    
    #tested
    def identity(self, size):
        result_str = call_func("identity", str(size))
        return Interoperability.to_py_mat(result_str)

    #tested
    def row_dim(self, py_matrix):
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        result_str = call_func("rowDim", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    def col_norm(self, py_matrix):
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        result_str = call_func("colNorm", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression
    
    #tested
    def row_norm(self, py_matrix):
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        result_str = call_func("rowNorm", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    #tested
    def col_dim(self, py_matrix):
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        result_str = call_func("colDim", ti_matrix)
        return result_str  # Assuming it returns a scalar value or expression

    #tested
    def row_swap(self, py_matrix, row1, row2):
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        result_str = call_func("rowSwap", ti_matrix + "," + str(row1) + "," + str(row2))
        return Interoperability.to_py_mat(result_str)

    #tested
    def ref(self, Matrix):
        ti_Matrix = Interoperability.to_ti_mat(Matrix)
        result_str = call_func("ref", ti_Matrix)
        return Interoperability.to_py_mat(result_str)

    #tested
    def rref(self, py_matrix, tol=None):
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        if tol is not None:
            result_str = call_func("rref", ti_matrix + "," + str(tol))
        else:
            result_str = call_func("rref", ti_matrix)
        return Interoperability.to_py_mat(result_str)

    #tested
    def simult(self, py_coeff_matrix, const_col_vector, tol=None):
        ti_coeff_matrix = Interoperability.to_ti_mat(py_coeff_matrix)
        ti_const_vector = Interoperability.to_ti_mat(const_col_vector)
        if tol is not None:
            result_str = call_func("simult", ti_coeff_matrix + "," + ti_const_vector + "," + str(tol))
        else:
            result_str = call_func("simult", ti_coeff_matrix + "," + ti_const_vector)
        return Interoperability.to_py_mat(result_str)

    #tested
    def transpose(self, py_matrix):
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        result_str = eval_expr("({})".format(ti_matrix))
        return Interoperability.to_py_mat(result_str)
    
    #tested
    def inverse(self, py_matrix):
        ti_matrix = Interoperability.to_ti_mat(py_matrix)
        result_str = eval_expr("({}^-1)".format(ti_matrix))
        return Interoperability.to_py_mat(result_str)