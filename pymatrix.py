import sys
if sys.platform == 'win32':
    from lib.symbols import Symbol

from ti_collections import TiCollections


class PyMatrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0
        self.shape = (self.rows, self.cols)
        self._current_row = 0
        self._current_col = 0

    @property
    def has_vars(self):
        if any(isinstance(x, Symbol) for row in self.data for x in row):
            return True
        if any(isinstance(x, str) for row in self.data for x in row):
            return True
        return False

    @property
    def T(self):
        return self.transpose()

    @property
    def is_row_vec(self):
        return self.rows == 1

    @property
    def is_col_vec(self):
        return self.cols == 1

    def __getitem__(self, indices):
        return self.data[indices[0]][indices[1]] if isinstance(indices, tuple) else self.data[indices]

    def __setitem__(self, indices, value):
        if isinstance(indices, tuple):
            row, col = indices
            self.data[row][col] = value
        else:
            self.data[indices] = value

    def __eq__(self, other):
        if isinstance(other, PyMatrix):
            return self.data == other.data
        elif isinstance(other, 'Vector'):
            return self.data == [other.data] if self.is_row_vec else self.data == [[x] for x in other.data]
        return False

    def __gt__(self, other):
        if isinstance(other, PyMatrix):
            return self.__gt_mat(other)
        elif isinstance(other, 'Vector'):
            return self.__gt_vec(other)
        return False

    def __lt__(self, other):
        if isinstance(other, 'CoreMatrix'):
            return not self.__gt_mat(other)
        elif isinstance(other, 'Vector'):
            return not self.__gt_vec(other)
        return False

    def __gt_mat(self, other_mat: 'PyMatrix'):
        return self.rows > other_mat.rows and self.cols > other_mat.cols

    def __gt_vec(self, other_vec):
        return self.rows > len(other_vec) if self.is_col_vec else self.cols > len(other_vec)

    def __len__(self):
        return self.rows

    def __eq__(self, other):
        if not isinstance(other, 'CoreMatrix'):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return all(
            self.data[i][j] == other.data[i][j]
            for i in range(self.rows)
            for j in range(self.cols)
        )

    def __list__(self):
        return self.data

    def __str__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    def add_vector(self, vector, position='column'):
        if position == 'column':
            if len(vector) != self.rows:
                return "Vector size must match the number of rows in the matrix to be added as a column"
            for i in range(self.rows):
                self.data[i].append(vector[i])
            self.cols += 1
        elif position == 'row':
            if len(vector) != self.cols:
                return "Vector size must match the number of columns in the matrix to be added as a row"
            self.data.append(vector.data)
            self.rows += 1
        else:
            return "Position must be either 'column' or 'row'"
        return self

    def add_column_vector(self, vector):
        if len(vector) != self.rows:
            raise ValueError(
                "Vector length must match the number of rows in the matrix.")
        for i in range(self.rows):
            self.data[i].append(vector[i])
        self.cols += 1
        self.shape = (self.rows, self.cols)

    def __add__(self, other):
        return PyMatrix([[a + b for a, b in zip(row1, row2)] for row1, row2 in zip(self.data, other.data)])

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return PyMatrix([[a - b for a, b in zip(row1, row2)] for row1, row2 in zip(self.data, other.data)])

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, 'Vector'):
            return self.__mul_vector(other)
        elif isinstance(other, PyMatrix):
            return self.__mul_matrix(other)
        elif isinstance(other, (int, float)):
            return self.__mul_scalar(other)
        else:
            raise TypeError("Unsupported type for multiplication")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul_matrix(self, other):
        return PyMatrix([[sum(self.data[i][k] * other.data[k][j] for k in range(self.cols)) for j in range(other.cols)] for i in range(self.rows)])

    def __mul_scalar(self, value: (int, float)):
        return PyMatrix([[self.data[i][j] * value for j in range(self.cols)] for i in range(self.rows)])

    def __mul_vector(self, vector: 'Vector'):
        from pyvector import PyVector
        if len(self) != len(vector):
            raise ValueError(
                "Vectors must have the same size for element-wise multiplication")
        return PyVector([self[i] * vector[i] for i in range(len(self))])

    def transpose(self):
        return PyMatrix([[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)])

    def scalar_multiply(self, scalar):
        return PyMatrix([[self.data[i][j] * scalar for j in range(self.cols)] for i in range(self.rows)])

    # Row Operations
    def row_swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        return self

    def row_mul(self, i, val):
        self.data[i] = [x * val for x in self.data[i]]
        return self

    def row_div(self, i, val):
        self.data[i] = [x / val for x in self.data[i]]
        return self

    def row_add(self, i, j, factor=1):
        self.data[i] = [x + factor * y for x,
                        y in zip(self.data[i], self.data[j])]
        return self

    def row_sub(self, i, j, factor=1):
        self.data[i] = [x - factor * y for x,
                        y in zip(self.data[i], self.data[j])]
        return self

    def __str__(self):
        return "[" + "\n".join([str(row) for row in self.data]) + "]"

    def __iter__(self):
        self._current_row, self._current_col = 0, 0
        return self

    def __next__(self):
        # If we've reached the end of the matrix, raise StopIteration
        if self._current_row == self.rows:
            raise StopIteration

        # Get the current item in the matrix
        item = self.data[self._current_row][self._current_col]

        # Update the current row and column indices for the next iteration
        self._current_col += 1
        if self._current_col == self.cols:
            self._current_col = 0
            self._current_row += 1

        return item

    def to_ti_col_vec(self):
        py_mat = list(self)
        return TiCollections.to_ti_col_vec(py_mat)

    def to_ti_row_vec(self):
        py_mat = list(self)
        return TiCollections.to_ti_row_vec(py_mat)
