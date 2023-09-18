import sys
if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../', '.'])

from ti_expression import TiExpression
from ti_collections import TiCollections
from ti_converters import *
from ti_formatting import mat_repr, display_matrix
from ti_traits import is_type
from dummy_types import *
from wrappers import extends_method_names
from polyfill import is_numeric
from ti_interop import tiexec
from matrix_tools import is_matrix, is_column_vector, is_row_vector, get_matrix_dimensions, get_symbolic_indices

if sys.platform == 'TI-Nspire':
    from wrappers import ensure_single_or_paired_type
    from wrappers import ensure_paired_type
    from eval_expr import eval_expr, call_func

from wrappers import debug_in_out
from collections import namedtuple

Pivot = namedtuple('Pivot', ['row', 'col'])

@extends_method_names
class TiMatrix(TiCollections):
    debug_in_out(enabled=True)

    def __init__(self, matrix_or_str: (str, list) = None, rows: int = None, fill=0):

        if isinstance(matrix_or_str, int) and rows and isinstance(rows, int):
            matrix_or_str = [
                [0 for _ in range(matrix_or_str)] for _ in range(rows)]
        elif not matrix_or_str:
            matrix_or_str = [[0]]
        else:
            matrix_or_str = to_py_mat(matrix_or_str)
        # self.ti_matrix = self.to_ti_mat(matrix_or_str)
        # self.py_matrix = self.to_py_mat(self.ti_matrix)
        self.ti_matrix = to_ti_mat(matrix_or_str)
        self.py_matrix = to_py_mat(self.ti_matrix)
        self.data = self.py_matrix
        self.rows = len(self.data)  # self.row_dim()  #
        self.cols = len(self.data[0]) if self.py_matrix else 0
        self.square = self.rows == self.cols
        self._current_row = 0
        self._current_col = 0

    def __isinstance__(self, obj):
        return isinstance(obj, TiMatrix)

    @property
    def is_numeric(self):
        return all(is_numeric(c) for r in self.data for c in r)

    @property
    def non_zero_row_count(self):
        return sum(1 for row in self.data if any(c != 0 for c in row))

    @property
    def T(self) -> 'TiMatrix':
        return self.transpose()

    def __mul__(self, other):
        if isinstance(other, list) and len(other) != self.cols:
            other = other[0]

        try:
            return TiMatrix(tiexec("({})*({})".format(self.ti_matrix, other)))
        except TypeError:
            print(
                "TypeError: unsupported operand type(s) for *: '{}' and '{}'".format(type(self), type(other)))

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

    def abs(self) -> 'TiMatrix':
        return TiMatrix(tiexec("abs", self.ti_matrix))

    def expand(self, var=None) -> 'TiMatrix':
        return TiMatrix(tiexec("expand", self.ti_matrix))

    def factor(self, var=None) -> 'TiMatrix':
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
        
        matrix = to_ti_col_vec(matrix)
        return TiMatrix(tiexec("augment", self.ti_matrix + "," + matrix))

    def col_augment(self, matrix) -> 'TiMatrix':
        """
            Returns a new py_matrix1 that is `py_matrix2
            appended to py_matrix1`. The matrices must
            have equal column dimensions, and
            `py_matrix2 is appended to py_matrix1 as new
            rows`. Does not alter py_matrix1 or py_matrix2
        """
        if is_type(matrix, (PyMat, TiList)):
            ti_col_vec = to_ti_col_vec(matrix)
        return TiMatrix(tiexec("colAugment", self.ti_matrix, ti_col_vec))

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

    def lcm(self, matrix) -> 'TiMatrix':
        """
            Returns the least common multiple of the
            elements in the matrix.
        """
        if TiCollections.is_py_mat(matrix):
            matrix = TiCollections.to_ti_mat(matrix)
        return TiMatrix(tiexec("lcm", self.ti_matrix, matrix))

    def norm(self) -> TiExpression:
        """
            Returns the maximum of the sums of the
            absolute values of the elements in the
            columns in Matrix.
        """
        return TiExpression(tiexec("norm", self.ti_matrix))

    def sub_mat(self, start_row=None, start_col=None, end_row=None, end_col=None) -> 'TiMatrix':
        """
            Returns the specified submatrix.
            Defaults: start_row=1, start_col=1,
            end_row=last row, end_col=last column
        """
        args = [str(arg) for arg in [start_row, start_col,
                                     end_row, end_col] if arg is not None]
        return TiMatrix(tiexec("subMat", self.ti_matrix + "," + ",".join(args)))

    @staticmethod
    def construct_mat(expr, var1: str, var2: str, num_rows: int, num_cols: int) -> 'TiMatrix':
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

    @staticmethod
    def rand_mat(num_rows: int, num_cols: int) -> 'TiMatrix':  # working
        return TiMatrix(tiexec("randMat", num_rows, num_cols))

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
        # return TiMatrix(call_func("abs", self.ti_matrix))
        return TiMatrix(tiexec("eigVc", self.ti_matrix))

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

    def median(self, matrix=None) -> 'TiMatrix':
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

    # check

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
        return TiMatrix(tiexec("eigVl", self.ti_matrix))

    def floor(self) -> 'TiMatrix':
        return TiMatrix(tiexec("floor", self.ti_matrix))

    def det(self, tol=None) -> TiExpression:
        if tol is not None:
            return TiExpression(tiexec("det", self.ti_matrix + "," + str(tol)))
        else:
            return TiExpression(tiexec("det", self.ti_matrix))

    def diag(self) -> 'TiMatrix':
        return TiMatrix(tiexec("diag", self.ti_matrix))

    def row_add(self, sum_with_row, sum_to_row) -> 'TiMatrix':
        """
            Returns a copy of matrix with row
            sum_to_row replaced by the sum of rows
            sum_with_row and sum_to_row.
        """
        return TiMatrix(tiexec("rowAdd", self.ti_matrix + "," + str(sum_with_row) + "," + str(sum_to_row)))

    def imag(self) -> 'TiMatrix':
        return TiMatrix(tiexec("imag", self.ti_matrix))

    def int(self) -> 'TiMatrix':
        return TiMatrix(tiexec("int", self.ti_matrix))

    def int_div(self, matrix) -> 'TiMatrix':
        """
            Returns the signed integer part of
            (Number1 ÷ Number2).
            For lists and matrices, returns the signed
            integer part of (argument 1 ÷ argument 2)
            for each element pair.
        """
        if TiCollections.is_py_mat(matrix):
            matrix = TiMatrix(matrix)
        return TiMatrix(tiexec("intDiv", self.ti_matrix, matrix))

    # TODO fix
    def row_sub(self, row_to_subtract: int, row_to_target: int, factor=1):

        row_subtract_values = self.get_row(row_to_subtract)
        row_subtract_target = self.get_row(row_to_target)

        sub_matrix = TiCollections.to_ti_mat(row_subtract_values)
        tar_matrix = TiCollections.to_ti_mat(row_subtract_target)

        result_str = tiexec(
            "{}-{}*{}".format(tar_matrix, sub_matrix, factor))
        result_row = TiCollections.to_py_mat(result_str)[0]

        result_py_matrix = [row for row in self.py_matrix]
        result_py_matrix[row_to_target - 1] = result_row

        return TiMatrix(result_py_matrix)

    def m_row(self, expr, row_idx) -> 'TiMatrix':
        """
            Returns a copy of the matrix with each
            element in row row_idx multiplied
            by `expr`.

        """
        return TiMatrix(tiexec("mRow", str(expr) + "," + self.ti_matrix + "," + str(row_idx)))

    def m_row_add(self, expr, mulexpr_row, update_row_idx) -> 'TiMatrix':
        """
            Returns a copy of the matrix with each
            element in row the update_row of replaced
            with:
            expr • mulexpr_row + update_row_idx
        """
        args = (str(expr), self.ti_matrix, str(
            mulexpr_row), str(update_row_idx))
        result_str = tiexec("mRowAdd", *args)
        # result_str = tiexec("mRowAdd", str(expr) + "," + self.ti_matrix + "," + str(mulexpr_row) + "," + str(update_row_idx))
        return TiMatrix(result_str)

    # @ensure_paired_type(allowed_types=[int])
    @staticmethod
    def new(rows: int, cols: int):
        return TiMatrix(tiexec("newMat", rows, cols))

    def eye(self, size: int) -> 'TiMatrix':
        return TiMatrix.identity(size)

    @staticmethod
    def identity(size: int) -> 'TiMatrix':
        return TiMatrix(tiexec("identity", size))

    def col_norm(self) -> TiExpression:
        return TiExpression(tiexec("colNorm", self.ti_matrix))

    def row_norm(self) -> TiExpression:
        return TiExpression(tiexec("rowNorm", self.ti_matrix))

    def col_dim(self) -> int:
        return int(tiexec("colDim", self.ti_matrix))

    def row_dim(self) -> int:
        return int(tiexec("rowDim", self.ti_matrix))

    def row_swap(self, row1, row2) -> 'TiMatrix':
        return TiMatrix(tiexec("rowSwap", self.ti_matrix, row1, row2))

    def get_row(self, row_idx) -> 'TiMatrix':
        if row_idx > self.rows:
            print("Row index out of range")
        return TiMatrix(tiexec("{}[{}]".format(self.ti_matrix, row_idx)))

    def get_col(self, col_idx):
        if col_idx > self.cols:
            print("Column index out of range")
        args = (self.ti_matrix, 1, col_idx, self.cols, col_idx)
        return TiMatrix(tiexec("subMat", *args))

    def real(self) -> 'TiMatrix':
        """
            Returns the real parts of all elements.
            Note: All undefined variables are treated as
            real variables. See also imag()
        """
        return TiMatrix(tiexec("real", self.ti_matrix))

    def ref(self):
        return TiMatrix(tiexec("ref", self.ti_matrix))

    def rref(self, tol=None) -> 'TiMatrix':
        if tol is not None:
            return TiMatrix(tiexec("rref", self.ti_matrix + "," + str(tol)))
        else:
            return TiMatrix(tiexec("rref", self.ti_matrix))

    # TODO fix
    def simult(self, const_vector, *args, tol=None):
        # ti_coeff_matrix = TiCollections.to_ti_mat(py_coeff_matrix)
        if args:
            constants = ']['.join([str(arg) for arg in args])
            constants = str(const_vector) + '][' + constants
            constants = '[[' + constants + ']]'
        else:
            constants = to_py_col_vec(constants)
            constants = to_ti_mat(constants)

        if tol is not None:
            result_str = tiexec(
                "simult", self.ti_matrix + "," + constants + "," + str(tol))
        else:
            result_str = tiexec(
                "simult", self.ti_matrix + "," + constants)
        return TiMatrix(result_str)

    def ipart(self) -> 'TiMatrix':
        return TiMatrix(tiexec("ipart", self.ti_matrix))

    def transpose(self) -> 'TiMatrix':
        return TiMatrix(tiexec("{}@t".format(self.ti_matrix)))

    def inverse(self) -> 'TiMatrix':
        return TiMatrix(tiexec("({}^-1)".format(self.ti_matrix)))

    def trace(self) -> TiExpression:
        """
            Returns the trace (sum of all the elements
            on the main diagonal) of squareMatrix.
        """
        return TiExpression(tiexec("trace", self.ti_matrix))
    
    def zero_rows(self):
        return [i+1 for i in range(self.rows) if all(c == 0 for c in self.data[i])]
    
    
        
        
    
    def pivots(self):
        """
        Find the pivot positions in a matrix in RREF.

        :param matrix: 2D list of numbers representing the matrix in RREF
        :return: list of tuples where each tuple contains the row and column index of a pivot
        """
        pivot_positions = []

        for i, row in enumerate(self.data):
            for j, val in enumerate(row):
                if val == 1:  # We found a pivot in this row
                    pivot_positions.append(Pivot(i+1, j+1))
                    break  # Move to the next row

        return pivot_positions

    def rank(self) -> int:
        return len(self.pivots())
    
    def nullity(self) -> int:
        return self.cols - self.rank()

    def is_numeric(self):
        return all(isinstance(col, (int, float)) for row in self.data for col in row)

    def is_symbolic(self):
        return not self.is_numeric()

    def __repr__(self):
        return mat_repr(self.data)

    def __str__(self):
        return self.ti_matrix

    def perform_tests():
        if sys.platform != 'TI-Nspire':
            print('Testing only available on TI-Nspire')
            pass

        py_mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        py_mat2 = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]
        ti_mat = TiMatrix(py_mat)
        assert ti_mat.is_numeric
        assert ti_mat.cols == 3
        assert ti_mat.rows == 3
        assert ti_mat.square == True
        assert ti_mat.non_zero_row_count == 3
        
        ti_mat2 = TiMatrix(py_mat2)
        print(ti_mat2.zero_rows())
        print(ti_mat2.pivots())
        print(ti_mat2.rank())
    @staticmethod
    def eye(size: int) -> 'TiMatrix':
        return TiMatrix(tiexec("identity", size))


if __name__ == '__main__':
    
    TiMatrix.perform_tests()    