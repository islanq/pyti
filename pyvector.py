
from ti_collections import TiCollections
class VecorSizeError(Exception):
    pass

class PyVector:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        
    @property
    def is_row_vector(self):
        return True  # Assuming all Vectors are row vectors by default
    
    @property
    def is_column_vector(self):
        return not self.is_row_vector  # The opposite of is_row_vector

   
    
    # You can also implement methods to allow a Vector to be easily converted to a CoreMatrix
    def to_core_matrix(self, as_row=True):
        if as_row:
            return self.to_row_matrix()
        else:
            return self.to_col_matrix()
        
    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, value):
        self.data[index] = value
        
    def __eq__(self, other):
        if isinstance(other, PyVector):
            return self.data == other.data
        elif isinstance(other, CoreMatrix):
            if other.rows == 1:
                return self.data == other.data[0]
            elif other.cols == 1:
                return self.data == [row[0] for row in other.data]
        return False
    
    def __len__(self):
        return self.size
    
    def __add__(self, other):
        if len(self) != len(other):
            raise VecorSizeError("Vectors must be of the same size")
        return PyVector([self[i] + other[i] for i in range(len(self))])
    
    def __sub__(self, other):
        if len(self) != len(other):
            raise VecorSizeError("Vectors must be of the same size")
        return PyVector([self[i] - other[i] for i in range(len(self))])
    
    def __mul__(self, other):
        if isinstance(other, PyVector):
            return self.__mul_vector(other)
        elif isinstance(other, CoreMatrix):
            return self.__mul_matrix(other)
        elif isinstance(other, (int, float)):
            return self.__mul_scalar(other)
        else:
            raise TypeError("Unsupported type for multiplication")
            
    def __mul_vector(self, other):
        if other.size != self.size:
            raise ValueError("Vectors must be of the same size")
        return sum([self[i] * other[i] for i in range(len(self))])

    def __mul_matrix(self, matrix):
        if isinstance(matrix, CoreMatrix):
            if len(self) != matrix.rows:
                raise ValueError("Vector size must match the number of rows in the matrix for multiplication")
            
            result = [0] * matrix.cols
            for j in range(matrix.cols):
                sum = 0
                for i in range(matrix.rows):
                    sum += self[i] * matrix[i][j]
                result[j] = sum
            return PyVector(result)
        else:
            raise TypeError("Expected a CoreMatrix for multiplication")
    
    def __mul_scalar(self, value: (int, float)):
        return PyVector([x * value for x in self.data])
    
    def __rmul__(self, other: (int, float, 'PyVector')):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            return "Can only divide by a scalar"
        if other == 0:
            return "Cannot divide by zero"
        return PyVector([x / other for x in self.data])
    
    def __eq__(self, other):
        if isinstance(other, PyVector):
            return self.data == other.data
        elif isinstance(other, CoreMatrix):
            return self.data == other.data[0] if other.rows == 1 else self.data == [row[0] for row in other.data]
        return False
    
    def __str__(self):
        return str(self.data)
        return "<" + ", ".join(map(str, self.data)) + ">"
    
    def __list__(self):
        return self.data
    
    def dot(self, other):
        if self.size != other.size:
            raise ValueError("Vectors must be of the same size")
        return sum(x * y for x, y in zip(self.elements, other.elements))

    def cross(self, other):
        if self.size != 3 or other.size != 3:
            raise ValueError("Cross product is only defined for 3D vectors")
        x1, y1, z1 = self.elements
        x2, y2, z2 = other.elements
        return PyVector([y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - y1 * x2], self.is_column)

    def magnitude(self):
        return sum(x ** 2 for x in self.elements) ** 0.5

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return self / mag

    def project_onto(self, other):
        return other.normalize() * (self.dot(other.normalize()))
    
    def to_row_matrix(self):
        return CoreMatrix([self.data])  # Wrap the data in another list to make it a 2D list
    
    # New method
    def to_col_matrix(self):
        from pymatrix import PyMatrix
        return PyMatrix([[x] for x in self.data]) # Each element becomes its own row, making it a column matrix
    
    def to_ti_col_vec(self):
        py_mat = list(self.to_col_matrix())
        return TiCollections.to_ti_col_vec(py_mat)
    
    def to_ti_row_vec(self):
        py_mat = list(self.to_row_matrix())
        return TiCollections.to_ti_row_vec(py_mat)
    
    
# v = Vector([1, 2, 3])
# print(v.to_col_matrix())
# print(isinstance(v.to_col_matrix(), Vector))
# print(v.to_row_matrix())