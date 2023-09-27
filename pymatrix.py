from collections import namedtuple
import sys

if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../', '.'])

# from ti_collections import TiCollections
from pyvector import PyVector
from ti_matrix import TiMatrix
from ti_converters import to_py_row_vec, to_py_col_vec, to_ti_mat
from matrix_tools import apply_percise_numbers
from listlike2d import ListLike2D
from ti_formatting import most_accurate
from character_scripting import char_subscript
from polyfill import map_replace

Pivot = namedtuple('Pivot', ['row', 'col'])


def enforces_symbolic(func):
    def wrapper(self, *args, **kwargs):
        if self._allnumeric:
            return func(self, *args, **kwargs)
        classname = self.__class__.__name__
        print("{}.{} is not supported for symbolic matrices".format(
            classname, func.__name__))
    return wrapper


def index_adjuster(func):
    def wrapper(self, *args, **kwargs):
        if not self._zero_based:
            args = tuple(arg - 1 if i < 2 and isinstance(arg, int)
                         else arg for i, arg in enumerate(args))
        return func(self, *args, **kwargs)
    return wrapper

class PyMatrix:...
class PyMatrix(ListLike2D):

    def __init__(self, data, cols=None, fill=0, zero_based=False):
        self.data = data
        super().__init__(data, cols, fill)
        self._allnumeric = all(isinstance(x, (int, float))
                               for row in self.data for x in row)
        self._longest = max(len(str(x)) for row in self.data for x in row)
        self._zero_based = zero_based
        self._pivots = None
        self._rref = None

    def clone(self):
        data = self.clone_data()
        return PyMatrix(data)

    @enforces_symbolic
    def REF(self, tol=1e-10):

        def zero_below(matrix, pivot_row: int, pivot_col: int) -> None:
            """Zero out all entries below the pivot in the same column."""
            pivot_val = matrix[pivot_row][pivot_col]
            for i in range(pivot_row + 1, len(matrix)):
                factor = matrix[i][pivot_col] / pivot_val
                matrix[i] = [a - factor * b for a,
                             b in zip(matrix[i], matrix[pivot_row])]

        def normalize_row(row, idx: int) -> list[float]:
            """Normalize the row by the value at the given index."""
            factor = row[idx]
            return [e / factor for e in row]

        def swap_rows(matrix, idx1: int, idx2: int) -> None:
            """Swap the rows at the given indices in the matrix."""
            matrix[idx1], matrix[idx2] = matrix[idx2], matrix[idx1]

        data = self.data
        rows, cols = len(data), len(data[0])
        pivots = []

        row = 0
        for col in range(cols):
            # Find the row with the maximum absolute value in the current column from the remaining rows
            max_row = max(range(row, rows), key=lambda i: abs(
                data[i][col]), default=row)

            # Swap the current row with the row having the maximum element in the current column
            swap_rows(data, row, max_row)

            # Skip if the column contains only zeros
            if abs(data[row][col]) < tol:
                continue

            # Make the diagonal element 1
            data[row] = normalize_row(data[row], col)

            pivots.append((row, col))

            # Make other elements in the column 0 (only below the pivot)
            zero_below(data, row, col)

            row += 1
            if row >= rows:
                break

        # Set very small values to zero
        for r in range(rows):
            for c in range(cols):
                if abs(data[r][c]) < tol:
                    data[r][c] = 0.0

        return PyMatrix(data), pivots

    def RREF(self, tol=1e-10):

        def zero_below(matrix, pivot_row: int, pivot_col: int) -> None:
            """Zero out all entries below the pivot in the same column."""
            pivot_val = matrix[pivot_row][pivot_col]
            for i in range(pivot_row + 1, len(matrix)):
                factor = matrix[i][pivot_col] / pivot_val
                matrix[i] = [a - factor * b for a,
                             b in zip(matrix[i], matrix[pivot_row])]

        def zero_above(matrix, pivot_row: int, pivot_col: int) -> None:
            """Zero out all entries above the pivot in the same column."""
            pivot_val = matrix[pivot_row][pivot_col]
            for i in range(pivot_row):
                factor = matrix[i][pivot_col] / pivot_val
                matrix[i] = [a - factor * b for a,
                             b in zip(matrix[i], matrix[pivot_row])]

        def normalize_row(row, idx: int) -> list[float]:
            """Normalize the row by the value at the given index."""
            factor = row[idx]
            return [e / factor for e in row]

        def swap_rows(matrix, idx1: int, idx2: int) -> None:
            """Swap the rows at the given indices in the matrix."""
            matrix[idx1], matrix[idx2] = matrix[idx2], matrix[idx1]

        data = [row[:] for row in self.data]
        rows, cols = self.dims  # len(data), len(data[0])
        pivots = []

        row = 0
        for col in range(cols):
            # Find the row with the maximum absolute value in the current column from the remaining rows
            max_row = max(range(row, rows), key=lambda i: abs(
                data[i][col]), default=row)

            # Swap the current row with the row having the maximum element in the current column
            swap_rows(data, row, max_row)

            # Skip if the column contains only zeros
            if abs(data[row][col]) < tol:
                continue

            # Make the diagonal element 1
            data[row] = normalize_row(data[row], col)

            pivots.append(Pivot(row, col))

            # Make other elements in the column 0
            zero_below(data, row, col)
            zero_above(data, row, col)

            row += 1
            if row >= rows:
                break

        # Set very small values to zero
        for r in range(rows):
            for c in range(cols):
                if abs(data[r][c]) < tol:
                    data[r][c] = 0.0

        self._pivots = pivots
        self._rref = PyMatrix(data)
        return self._rref, self._pivots

# region Arithmetic Dunder Methods

    def __mul__(self, other):
        if isinstance(other, list):
            B = PyMatrix(other)
        elif hasattr(other, 'data') and isinstance(other.data, list):
            B = PyMatrix(other.data)
        elif isinstance(other, PyMatrix):
            B = other
        else:
            B = None

        if isinstance(other, (int, float)):
            return self.__mul_scalar(other)
        elif B is not None:
            return self.__mul_matrix(B)
        else:
            raise TypeError("Unsupported type for multiplication")

        # A = self.clone_data()
        # B = other.clone_data()
        # # Initialize the result matrix with zeros and an intermediate display matrix
        #

    def __mul_matrix(self, other):
        """Multiply this matrix by another matrix."""
        if self.dims.cols != other.dims.rows:
            raise ValueError("Matrices cannot be multiplied")
        A = self.clone_data()
        B = other.clone_data()

        return PyMatrix([[sum(A[i][k] * B[k][j] for k in range(self.dims.cols)) for j in range(other.dims.cols)] for i in range(self.dims.rows)])

    def __mul_scalar(self, other):
        """Multiply this matrix by a scalar."""
        data = self.clone_data()
        return PyMatrix([[other * elem for elem in row] for row in data])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        result = self * other
        self.data = result.data
        return self

    # C = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    #     for i in range(len(A)):
    #         for j in range(len(B[0])):
    #             for k in range(len(B)):
    #                 C[i][j] += A[i][k] * B[k][j]

    #     return PyMatrix(C)

    def __add__(self, other):
        A = self.clone_data()
        B = other.clone_data()
        return PyMatrix([[a + b for a, b in zip(row1, row2)] for row1, row2 in zip(A, B)])

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        A = self.clone_data()
        B = other.clone_data()
        return PyMatrix([[a - b for a, b in zip(row1, row2)] for row1, row2 in zip(A, B)])

    def __rsub__(self, other):
        return self.__sub__(other)

# endregion Arithmetic Dunder Methods

    def pivots(self) -> list:
        """_summary_
            Pivots are the leading 1's in the RREF
        Returns:
            list: _description_ pivot positions in the matrix columns
        """
        if self._pivots is None:
            self._pivots = self.RREF()[1]
        return self._pivots

    def rank(self) -> int:
        """_summary_
            Rank is the number of pivots in the matrix.
            leading 1's in the RREF
        Returns:
            int: _description_ number of pivots in the matrix after RREF
        """
        return len(self.pivots())

    def nullity(self, message=False) -> int:
        """
            Returns the nullity of the matrix. 
            columns - rank = nullity
        """
        if message:
            print("nullity = columns - rank")
        return self.dims.cols - self.rank()

    # region Row Operations

    @index_adjuster
    def row_swap(self, i: int, j: int) -> PyMatrix:
        self.data[i], self.data[j] = self.data[j], self.data[i]
        return self

    @index_adjuster
    def row_mul(self, i: int, val: (int, float)) -> PyMatrix:
        """ multiply row i by val """
        self.data[i] = [x * val for x in self.data[i]]
        return self

    @index_adjuster
    def row_div(self, i: int, val: int | float) -> PyMatrix:
        """ divide row i by val """
        self.data[i] = [x / val for x in self.data[i]]
        return self

    @enforces_symbolic
    @index_adjuster
    def row_add(self, i: int, j: int, factor: (int, float) = 1) -> PyMatrix:
        """ add row j to row i with factor """
        self.data[i] = [x + factor * y for x,
                        y in zip(self.data[i], self.data[j])]
        return self

    @index_adjuster
    def row_sub(self, i: int, j: int, factor: (int, float) = 1) -> PyMatrix:
        """ subtract row j from row i with factor """
        self.data[i] = [x - factor * y for x,
                        y in zip(self.data[i], self.data[j])]
        return self

    def _adjust_indices(self, idx1, idx2=None):
        if idx2 is None:
            idx2 = idx1
        if self._zero_based:
            idx1 -= 1
            idx2 -= 1
        return idx1, idx2
    # endregion Row Operations

    def span(self):
        """_summary_
            Returns True if the matrix spans R^r, False otherwise.
        Args:
            self (_type_): _description_
            r (int): _description_

        Returns:
            bool: _description_
        """
        return self.rank()

    def lin_indep_cols(self):
        return [pivot.col for pivot in self.pivots()]

    def lin_indep_rows(self):
        return [pivot.row for pivot in self.pivots()]

    def pivot_cols(self):
        return self.lin_indep_cols()

    def pivot_rows(self):
        return self.lin_indep_rows()

    def free_var_cols(self):
        return [col for col in range(self.dims.cols) if col not in self.lin_indep_cols()]

    def row_space_basis(self):
        return PyMatrix([self.data[row] for row in self.lin_indep_rows()])

    def col_space_basis(self):
        return self.get_cols(*self.lin_indep_cols())

    def subspace_basis(self):
        return self.get_cols(*self.pivot_cols())

    def subspace_dimension(self):
        return self.rank()

    def summary(self, rref=True, rank=True, nullity=True, spans=True, lin_indep=True, free_vars=True):
        print(self.RREF()[0])
        print("Write down the RREF of the matrix")

        input("Press any key to continue...")

        print("rank: {}".format(self.rank()))
        print("nullity: {}".format(self.nullity()))
        print("Spans: R^{}".format(self.span()))

        input("Press any key to continue...")

        if self.rank() == self.dims.cols:
            print("LI: Linearly Independent")
            print("Lin. Ind. Cols: {}".format(", ".join(str(col+1)
                  for col in self.lin_indep_cols())))
        else:
            print("LI: Linearly Dependent")
            print("Free Cols: {}".format(", ".join(str(col+1)
                  for col in self.free_var_cols())))
            print("Free Col Cnt: {}".format(len(self.free_var_cols())))

            input("Press any key to continue...\n")

            non_trivial = self.non_trivial_solutions()
            print(non_trivial)
            if '=s' in non_trivial and '=t' in non_trivial:
                print("If you have S & T:\nset S = 1 and T = 0,\nthen S = 0 and T = 1")
            print("Lin. Ind. Cols: {}".format(", ".join(str(col+1)
                  for col in self.lin_indep_cols())))

    def non_trivial_solutions(self, tol=1e-10):
        replacement_map = {
            ' ': '',
            'u': 's',
            '+-': '-',
        }

        # Step 1: Identify the free variables and get the RREF matrix and its dimensions
        rref, pivots = self.RREF()
        rows, cols = rref.dims
        pivot_cols = [col for row, col in pivots]
        # Using characters 't', 'u', ...
        free_vars = [chr(116 + i) for i in range(cols - len(pivot_cols))]

        # Step 2: Create expressions for each row in the RREF matrix
        relations = []
        for row in range(rows):
            relation = " + ".join(
                "{}x{}".format(most_accurate(
                    rref.data[row][col]), str(col + 1))
                for col in range(cols) if abs(rref.data[row][col]) > tol
            )
            if relation:
                relations.append("0 = " + relation)

        # Step 3: Add expressions for the free variables
        for i in range(cols):
            if i not in pivot_cols:
                relations.append("x{} = {}".format(
                    str(i + 1), free_vars[i - len(pivot_cols)]))

        # Combine the relations into a single string

        solution_str = ", ".join(relations)
        solution_str = map_replace(solution_str, **replacement_map)
        return solution_str

    def get_cols(self, *cols):
        return PyMatrix(super().get_cols(*cols).data)

    def get_rows(self, *rows):
        return PyMatrix(super().get_rows(*rows).data)

    def determinant(self):
        matrix = self.clone_data()
        n = len(matrix)

        det = 1

        for i in range(n):
            max_el = abs(matrix[i][i])
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix[k][i]) > max_el:
                    max_el = abs(matrix[k][i])
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            det *= matrix[i][i]
            for k in range(i + 1, n):
                matrix[k][i] /= matrix[i][i]
                for j in range(i + 1, n):
                    matrix[k][j] -= matrix[k][i] * matrix[i][j]

        return most_accurate(det)

    def inverse(self):
        n = self.dims.rows
        matrix = self.clone_data()

        # Augment the matrix with the identity matrix
        for i in range(n):
            matrix[i] += [0] * i + [1] + [0] * (n - i - 1)

        # Apply Gauss-Jordan elimination
        for i in range(n):
            # Find the row with the maximum element in column i and swap with row i
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

            # Make the diagonal element of the current row equal to 1
            div = matrix[i][i]
            matrix[i] = [x / div for x in matrix[i]]

            # Make the elements above and below the diagonal element equal to 0
            for j in range(n):
                if j != i:
                    ratio = matrix[j][i] / matrix[i][i]
                    matrix[j] = [x - ratio * y for x,
                                 y in zip(matrix[j], matrix[i])]
            inverse_matrix = [row[n:] for row in matrix]
        # print("Inverse matrix:")
        # for row in inverse_matrix:
        #     print(row)

        return apply_percise_numbers(inverse_matrix)

    def inverse_back(self):
        n = self.dims.rows
        matrix = self.clone_data()

        # Augment the matrix with the identity matrix
        for i in range(n):
            matrix[i] += [0] * i + [1] + [0] * (n - i - 1)

        # Apply Gauss-Jordan elimination
        # Forward elimination
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

            for j in range(i + 1, n):
                ratio = matrix[j][i] / matrix[i][i]
                for k in range(2 * n):
                    matrix[j][k] -= ratio * matrix[i][k]

        # Back substitution
        for i in range(n-1, -1, -1):
            for j in range(i-1, -1, -1):
                ratio = matrix[j][i] / matrix[i][i]
                for k in range(2 * n):
                    matrix[j][k] -= ratio * matrix[i][k]

            # Divide the row by the pivot element
            div = matrix[i][i]
            for k in range(2 * n):
                matrix[i][k] /= div

        # Extract the inverse matrix and apply precision numbers
        return apply_percise_numbers([row[n:] for row in matrix])

    def inverse2(self):
        n = self.dims.rows
        matrix = self.clone_data()

        # Augment the matrix with the identity matrix
        for i in range(n):
            matrix[i] += [0] * i + [1] + [0] * (n - i - 1)

        # Apply Gauss-Jordan elimination
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, n):
                ratio = matrix[j][i] / matrix[i][i]
                for k in range(i, 2 * n):
                    matrix[j][k] -= ratio * matrix[i][k]
            for j in range(n):
                if j != i:
                    ratio = matrix[j][i] / matrix[i][i]
                    for k in range(2 * n):
                        matrix[j][k] -= ratio * matrix[i][k]
            div = matrix[i][i]
            for k in range(2 * n):
                matrix[i][k] /= div

        # Extract the inverse matrix
        # return PyMatrix([row[n:] for row in matrix])
        return apply_percise_numbers([row[n:] for row in matrix])

    def __repr__(self):
        return self.__str__()

    def to_ti_col_vec(self):
        py_mat = list(self)
        py_mat = to_py_col_vec(py_mat)
        ti_mat = to_ti_mat(py_mat)
        return ti_mat

    def to_ti_row_vec(self):
        py_mat = list(self)
        py_mat = to_py_row_vec(py_mat)
        ti_mat = to_ti_mat(py_mat)
        return ti_mat


if __name__ == '__main__':

    mat_numeric1 = PyMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    mat_numeric2 = PyMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    mat_num_clone = mat_numeric1.clone()

    mat_identity_3x3 = PyMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    mat_identity_2x2 = PyMatrix([[1, 0], [0, 1]])
    mat_identity_4x4 = PyMatrix(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    # ensure that the matrices are equal
    assert (mat_numeric1 == mat_numeric2)
    assert (mat_numeric1 == mat_num_clone)

    # # ensure arithmetic operations work
    assert (mat_numeric1 + mat_numeric2 == mat_numeric1 + mat_numeric1)
    assert (mat_numeric1 - mat_numeric2 == mat_numeric1 - mat_numeric1)
    assert (mat_numeric1 * mat_numeric2 == mat_numeric1 * mat_numeric1)
    assert (mat_numeric1 * 2 == mat_numeric1 + mat_numeric1)
