from matrix_format import FormatterTemplate, decimal_to_frac_str
from queue_print import PrintManager


class Matrix:
  
  def __init__(self, matrix, aug_col=False):
    self.matrix = matrix
    self.m = len(matrix) # number of rows
    self.n = len(matrix[0]) if self.m else 0
    self.current_row = 0
    self.current_col = 0
    self.has_aug_col = aug_col
    self.pm = PrintManager()
    self.template = FormatterTemplate()
  
  @property
  def rows(self):
    return len(self.matrix)
  
  @property
  def cols(self):
    return len(self.matrix[0]) if self.m else 0
  
  def identity(self, n):
    return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])
  
  def __len__(self):
    return len(self.matrix)
  
  def __getitem__(self, indices):
    return self.matrix[indices[0]][indices[1]] if isinstance(indices, tuple) else self.matrix[indices]
    
  def __setitem__(self, indices, value):
    if isinstance(indices, tuple):
        row, col = indices
        self.matrix[row][col] = value
    else:
        self.matrix[indices] = value
  
  def __str__(self):
   return (self.template.format_matrix(self.matrix))
  
  @staticmethod
  def ensure_matrix_format(matrix_obj):
      """Convert input to matrix format if not an instance of the Matrix class."""
      return matrix_obj.matrix if isinstance(matrix_obj, Matrix) else matrix_obj

  def __add__(self, other):
      A = self.matrix
      B = self.ensure_matrix_format(other)
      
      # Check if matrices can be added
      if len(A) != len(B) or len(A[0]) != len(B[0]):
          print("Matrices must have the same dimensions")
          return None
      
      # Initialize the result matrix and an intermediate display matrix
      C = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]
      display = [["" for _ in range(len(A[0]))] for _ in range(len(A))]
      
      for i in range(len(A)):
          for j in range(len(A[0])):
              display[i][j] = "{}+{}".format(A[i][j], B[i][j])
              display[i][j] = display[i][j].replace("+-", "-")  # Correcting double negative
              C[i][j] = A[i][j] + B[i][j]
      
      # Display the addition steps
      compact_display = "["
      for i, v in enumerate(display):
          spacer = "[ " if i == 0 else " [ "
          compact_display += spacer + ", ".join(v) + " ],\n"
      compact_display = compact_display.rstrip(",\n") + "]"
      print(compact_display)

      return Matrix(C)

  def __sub__(self, other):
      A = self.matrix
      B = self.ensure_matrix_format(other)
      
      # Check if matrices can be subtracted
      if len(A) != len(B) or len(A[0]) != len(B[0]):
          print("Matrices must have the same dimensions")
          return None
      
      # Initialize the result matrix and an intermediate display matrix
      C = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]
      display = [["" for _ in range(len(A[0]))] for _ in range(len(A))]
      
      for i in range(len(A)):
          for j in range(len(A[0])):
              display[i][j] = "{}-{}".format(A[i][j], B[i][j])
              display[i][j] = display[i][j].replace("--", "+")  # Correcting double negative
              C[i][j] = A[i][j] - B[i][j]
      
      # Display the subtraction steps
      compact_display = "["
      for i, v in enumerate(display):
          spacer = "[ " if i == 0 else " [ "
          compact_display += spacer + ", ".join(v) + " ],\n"
      compact_display = compact_display.rstrip(",\n") + "]"
      print(compact_display)
      
      return Matrix(C)

  def __mul__(self, other):
    A = self.matrix
    B = other.matrix if isinstance(other, Matrix) else other
    
    # Check if matrices can be multiplied
    if len(A[0]) != len(B):
        print("Matrices cannot be multiplied")
        return None
    
    # Initialize the result matrix with zeros and an intermediate display matrix
    C = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    display = [["" for _ in range(len(B[0]))] for _ in range(len(A))]
    
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                # Update the intermediate display matrix
                if display[i][j]:
                    display[i][j] += "+"
                display[i][j] += "{}*{}".format(A[i][k], B[k][j])
                C[i][j] += A[i][k] * B[k][j]
    
    display = self.template.format_matrix(C)
    self.pm.add_to_queue(display)
    
    return Matrix(C)

  def __eq__(self, other):
    return self.matrix == other.matrix if isinstance(other, Matrix) else self.matrix == other

  def __ne__(self, other):
      return not self.__eq__(other)
  
  def __rmul__(self, other):
    return self.__mul__(other)
  
  def __pow__(self, power):
    """Computes the matrix raised to a given power."""
    if self.m != self.n:
        print("Matrix must be square for matrix exponentiation.")
        return None

    if power < 0:
        inverse = self.inverse()
        if not inverse:
          print("Matrix is singular. Cannot compute negative power.")
          return None
        return inverse ** (-power)
    return self.identity(self.m) if power == 0 else self * (self ** (power - 1))

  def __iter__(self):
    self.current_row, self.current_col = 0, 0
    return self

  def __next__(self):
    # If we've reached the end of the matrix, raise StopIteration
    if self.current_row == self.m:
        raise StopIteration

    # Get the current item in the matrix
    item = self.matrix[self.current_row][self.current_col]

    # Update the current row and column indices for the next iteration
    self.current_col += 1
    if self.current_col == self.n:
        self.current_col = 0
        self.current_row += 1

    return item

  def reshape(self, m, n):
    """Reshapes the matrix to the given dimensions."""
    if self.m * self.n != m * n:
        print("Cannot reshape {}x{} matrix to {}x{} matrix.".format(self.m, self.n, m, n))
        return None
    flattened = [item for sublist in self.matrix for item in sublist]
    new_matrix = [[flattened[i * n + j] for j in range(n)] for i in range(m)]
    return Matrix(new_matrix)

  def transpose(self):
    result = [[0 for _ in range(self.m)] for _ in range(self.n)]
    for i in range(self.m):
      for j in range(self.n):
        result[j][i] = self.matrix[i][j]
    
    return Matrix(result)

  def determinant(self):
    """
    Compute the determinant of a matrix.
    Uses recursion for matrices larger than 2x2.
    """
    if len(self.matrix) != len(self.matrix[0]):
        raise ValueError("The matrix must be square.")
    
    if len(self.matrix) == 1:
        return self.matrix[0][0]
    
    if len(self.matrix) == 2:
        return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
    
    det = 0
    for j in range(len(self.matrix)):
        sub_matrix = Matrix(self.submatrix(0, j))
        det += ((-1) ** j) * self.matrix[0][j] * self.determinant(sub_matrix)
    return det

  def cofactor(self, i, j):
    """
    Compute the cofactor of matrix at (i, j).
    Uses determinant of submatrix obtained by removing row i and column j.
    """
    
    sub_matrix = Matrix(self.submatrix(i, j))
    return ((-1) ** (i + j)) * sub_matrix.determinant()
  
  def matrix_of_cofactors(self):
    """Compute the matrix of cofactors."""
    return [[self.cofactor(i, j) for j in range(len(self.matrix))] for i in range(len(self.matrix))]

  def inverse(self):
    """Compute the inverse of a matrix."""
    det = self.determinant()
    if det == 0:
        raise ValueError("The matrix is singular and does not have an inverse.")
    
    cofactors = self.matrix_of_cofactors()
    adjugate = Matrix(list(map(list, zip(*cofactors))))  # Transpose the matrix of cofactors
    
    # Using the row_div method to divide each row by the determinant
    for i in range(len(adjugate.matrix)):
        adjugate._row_divide(i, det)
    
    return adjugate.matrix

  def get_aug_column(self):
    return [row[-1] for row in self.matrix] if self.has_aug_col else None

  def free_variables(self):
    return self.n - len(self.get_pivot_cols()) - (1 if self.has_aug_col else 0)

  @property
  def is_square(self):
    return self.m == self.n
  
  def is_symmetric(self):
    return self.is_square and all(self.matrix[i][j] == self.matrix[j][i] for i in range(self.m) for j in range(self.n))

  def get_num_pivots(self):
    return len(self.get_pivot_cols())

  def get_pivot_cols(self):
    return [col for row in range(self.m) for col in range(self.n) if self.matrix[row][col] == 1]


  def is_upper_triangular(self):
        """
        Check if the matrix is upper triangular.
        """
        for i in range(1, self.rows):
            for j in range(0, min(i, self.cols)):
                if self.matrix[i][j] != 0:
                    return False
        return True

  def upper_triangular_determinant(self):
      """
      Calculate the determinant of an upper triangular matrix.
      """
      if not self.is_upper_triangular():
          raise ValueError("Matrix is not upper triangular.")
      
      determinant = 1
      for i in range(self.rows):
          determinant *= self.matrix[i][i]
      return determinant

  def determinant_verbose(self):
    if self.rows != self.cols:
        raise ValueError("Matrix is not square")
    
    # Create a copy of the matrix for manipulation
    matrix_copy = [row.copy() for row in self.matrix]
    m = Matrix(matrix_copy)
    
    det = 1  # Starting value for determinant
    
    for j in range(m.cols):
        # Find a pivot (non-zero element) in column j and swap with current row if necessary
        if m.matrix[j][j] == 0:
            for i in range(j+1, m.rows):
                if m.matrix[i][j] != 0:
                    print(f"Swapping row {j} with row {i}")
                    m._row_swap(i, j)
                    det *= -1  # Swapping rows changes the sign of determinant
                    break

        # If no pivot is found, then determinant is zero
        if m.matrix[j][j] == 0:
            return 0

        det *= m.matrix[j][j]  # Multiply det by the diagonal element

        # Eliminate all entries below the pivot
        for i in range(j+1, m.rows):
            if m.matrix[i][j] != 0:
                factor = m.matrix[i][j] / m.matrix[j][j]
                print(f"Making zero at position {i},{j} by subtracting {factor:.2f} times row {j} from row {i}")
                m._row_subtract(i, j, factor)
    
    return det

  def determinant_old(self):
    if not self.is_square:
      return "Matrix must be square"
    
    if self.m == 1:
      return self.matrix[0][0]
    
    if self.m == 2:
      return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
    
    det = 0
    for j in range(self.n):
      det += ((-1) ** j) * self.matrix[0][j] * self.submatrix(0, j).determinant()
    
    return det

  def is_ref(self):
    """Check if a matrix is in Row Echelon Form (REF)"""
    last_leading_position = -1
    for row in self.matrix:
        leading_position = None
        for j, entry in enumerate(row):
            if entry != 0:
                leading_position = j
                # Check if leading entry is 1
                if entry != 1:
                    return False
                # Check if leading entry is to the right of the last row's leading entry
                if leading_position <= last_leading_position:
                    return False
                last_leading_position = leading_position
                break
    return True

  def is_rref(self):
    """Check if a matrix is in Reduced Row Echelon Form (RREF)"""
    if not self.is_ref():
        return False
    for i, row in enumerate(self.matrix):
        for j, entry in enumerate(row):
            if entry == 1:  # This is a leading entry
                # All other entries in the column should be zero
                if any(self.matrix[k][j] for k in range(len(self.matrix)) if k != i):
                    return False
                break
    return True
    
  def to_ref(self, rref_caller=False):
    if self.is_ref():
        if not rref_caller:
            print("Matrix is already in REF.")
        return
    
    matrix = self.matrix
    m, n = self.m, self.n

    # Forward elimination to get Row Echelon Form
    for i in range(m):
        max_row = i
        for k in range(i+1, m):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        if max_row != i:
            self._row_swap(i, max_row)

        # Check for zero pivot
        if matrix[i][i] == 0:
            continue
        # Normalize pivot row
        pivot = matrix[i][i]
        if pivot != 1:
            self._row_divide(i, pivot)
        # Eliminate other rows
        for k in range(i+1, m):
            factor = matrix[k][i]
            if factor != 0:
                self._row_subtract(k, i, factor)
                
    if not rref_caller:
        print("The matrix in Row Echelon Form (REF) is:")
        self.pm.add_to_queue(self.template.format_matrix(self.matrix))  

  def to_rref(self):
    """Refined method to manually convert the matrix to its Reduced Row Echelon Form (RREF)"""
    matrix = self.matrix
    m, n = len(matrix), len(matrix[0])
    
    lead = 0
    for r in range(m):
        if lead >= n:
            break
        i = r
        while matrix[i][lead] == 0:
            i += 1
            if i == m:
                i = r
                lead += 1
                if n == lead:
                    lead -= 1
                    break
        matrix[i], matrix[r] = matrix[r], matrix[i]
        lv = matrix[r][lead]
        if lv == 0:
            continue
        #matrix[r] = [mrx / float(lv) for mrx in matrix[r]]
        self._row_divide(r, lv)
        for i in range(m):
            if i != r:
                lv = matrix[i][lead]
                self._row_subtract(i, r, lv)
                #matrix[i] = [iv - lv*rv for rv,iv in zip(matrix[r], matrix[i])]
        lead += 1
    self.matrix = matrix
    self.pm.add_to_queue(self.template.format_matrix(self.matrix))
    return self.matrix

  def gaussian_elimination(self):
      matrix = self.matrix
      m, n = self.m, self.n
      last_col = n  # initially assume the matrix does not have an augmented column
      if self.has_aug_col:
          n = n - 1
      
      pivots = []
      for i in range(m):
          max_row = i
          for k in range(i+1, m):
              if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                  max_row = k
          if max_row != i:
              self._row_swap(i, max_row)
          
          if matrix[i][i] != 0:
              pivots.append(i)
          
          pivot = matrix[i][i]
          if pivot != 1 and pivot != 0:
              self._row_divide(i, pivot)
          
          for k in range(i+1, m):
              factor = matrix[k][i]
              if factor != 0:
                  self._row_subtract(k, i, factor)

      comments = []
      free_vars = set(range(n)) - set(pivots)
      for f in free_vars:
          comments.append(f"The {f+1} column contains no pivots, thus x_{f+1} is a free variable and the system has infinitely many solutions")

      num_solutions = 1 if not free_vars else float('inf')
      solutions = []
      for i in range(m):
          if all([cell == 0 for cell in matrix[i][:n]]) and matrix[i][last_col-1] != 0:
              solutions.append("The system has no solution.")
              comments.append(f"The last row is equivalent to 0={matrix[i][last_col-1]}, thus the system is inconsistent")
              return 0, solutions, comments

      if not free_vars:
          comments.append("There are no free variables and the system has a unique solution")
          x = [0 for _ in range(n)]
          for i in pivots[::-1]:
              x[i] = matrix[i][last_col-1]
              for j in range(i+1, n):
                  x[i] -= matrix[i][j] * x[j]
              solutions.append(f"x[{i+1}] = {x[i]}")

      if not solutions:
          solutions.append("The system has infinitely many solutions.")
      return num_solutions, solutions, comments
  
  # Row operations
  def _row_swap(self, i, j, display=True):
      """Swap rows i and j of the matrix."""
      self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
      print("R{} ↔ R{}".format(i+1, j+1))

  def _row_divide(self, i, val, display=True):
      """Divide row i by the value val."""
      if val == 0 or val is None:
        return
      
      self.matrix[i] = [self.matrix[i][j] / val for j in range(self.n)]
      print("R{} ← R{} / {}".format(i+1, i+1, decimal_to_frac_str(val)))
      print(self.template.format_row(self.get_row(i)))
      #print(" " + str(self.get_row(i)))

  def _row_multiply(self, i, val, display=True):
      self.matrix[i] = [self.matrix[i][j] * val for j in range(self.n)]
      #self.pm.add_to_queue(self.template.format_operation('mul', i, i, value=val))
      print("R{} ← R{} * {}".format(i+1, i+1, decimal_to_frac_str(val)))
      print(self.template.format_row(self.get_row(i)))
      #print(" " + str(self.get_row(i)))
      
  def _row_subtract(self, i, j, factor=1, display=True):
      """Subtract factor times row j from row i."""
      if factor is None:
        return
      self.matrix[i] = [self.matrix[i][k] - factor * self.matrix[j][k] for k in range(self.n)]
      #self.pm.add_to_queue(self.template.format_operation('sub', i, i, factor))
      print("R{} ← R{} - ({} * R{})".format(i+1, i+1, decimal_to_frac_str(factor), j+1))
      print(" " + str(self.get_row(i)))
        
  def _row_add(self, i, j, factor=1, display=True):
    """Add factor times row j to row i."""
    self.matrix[i] = [self.matrix[i][k] + factor * self.matrix[j][k] for k in range(self.n)]
    print("R{} ← R{} + ({} * R{})".format(i+1, i+1, decimal_to_frac_str(factor), j+1))

  def get_row(self, i):
    if 0 <= i < self.m:
      return self.matrix[i]
    raise IndexError("Row index out of range")

  def get_col(self, i):
    if 0 <= i < self.n:
        return [[row[i]] for row in self.matrix]
    raise IndexError("Column index out of range")

  def set_row(self, i, row):
    if 0 <= i < self.m:
      self.matrix[i] = row
      return
    raise IndexError("Row index out of range")

  def set_col(self, i, col):
    if 0 <= i < self.n:
        if isinstance(col, list) and isinstance(col[0], list):
            col = [row[0] for row in col]
        for j, val in enumerate(col):
            self.matrix[j][i] = val
        return
    raise IndexError("Column index out of range")

  @staticmethod
  def is_col_vector(vector):
    # a column vector is a list of lists with each inner list containing a single element
    return isinstance(vector, list) and isinstance(vector[0], list) and len(vector[0]) == 1
    
  def submatrix(self, i, j):
    """Return the submatrix formed by deleting the ith row and jth column."""
    return Matrix([row[:j] + row[j+1:] for row in (self.matrix[:i]+self.matrix[i+1:])])
  
  def lu_factorization(self):
      """
      Compute the LU factorization of a matrix using the Matrix class methods.
      """
      n = len(self.matrix)
      
      # Initialize L as identity matrix and U as a copy of the original matrix
      L = Matrix([[0]*n for _ in range(n)])
      U = Matrix([row.copy() for row in self.matrix])
      
      for i in range(n):
          L.matrix[i][i] = 1.0

      for j in range(n):
          # Update the values for U's upper triangle and L's lower triangle
          for i in range(j+1, n):
              if U.matrix[j][j] == 0:
                  raise ValueError("LU decomposition is not possible as the matrix is singular.")
              
              factor = U.matrix[i][j] / U.matrix[j][j]
              L.matrix[i][j] = factor
              
              # Subtract a multiple of row j from row i
              U._row_subtract(i, j, factor)
      
      return L, U
    
  def forward_substitution(self, L, b):
        """Solve Ly = b for y using forward substitution."""
        n = len(self.matrix)
        y = [0] * n
        y[0] = b[0] / L.matrix[0][0]
        for i in range(1, n):
            y[i] = (b[i] - sum(L.matrix[i][j] * y[j] for j in range(i))) / L.matrix[i][i]
        return y

  def backward_substitution(self, U, y):
      """Solve Ux = y for x using backward substitution."""
      n = len(self.matrix)
      x = [0] * n
      x[-1] = y[-1] / U.matrix[-1][-1]
      for i in range(n-2, -1, -1):
          x[i] = (y[i] - sum(U.matrix[i][j] * x[j] for j in range(i+1, n))) / U.matrix[i][i]
      return x

  def solve_system(self, b):
      ''' USAGE:
        A = Matrix([
          [1,3,-4],
          [1,0,-3],
          [-1, -15, 11]])

        L, U, Ly, Ux, x = A.solve_system([3,1,-8])
        print("L = " + str(L))
        print("U = " + str(U))
        print("Ly = " + str(Ly))
        print("Ux = " + str(Ux))
        print("x = " + str(x))
      '''
    
    
    
      # LU Factorization
      L, U = self.lu_factorization()
      
      # Solve for y in Ly = b
      y = self.forward_substitution(L, b)
      
      # Compute Ly for verification
      Ly = [sum(L.matrix[i][j] * y[j] for j in range(3)) for i in range(3)]
      
      # Solve for x in Ux = y
      x = self.backward_substitution(U, y)

      # Compute Ux for verification
      Ux = [sum(U.matrix[i][j] * x[j] for j in range(3)) for i in range(3)]

      return L.matrix, U.matrix, Ly, Ux, x
  # TODO Implement a proper linear system solver that handles the cases where we need s and t

def flatten(lst):
    """Flatten a list of lists into a single list."""
    return [item for sublist in lst for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]

def convert_to_matrix(s: str) -> list:
    # Handle the format without commas between lists
    s = s.replace("][", "],[")
    # Handle the semicolon-separated format
    if not s.startswith("["):
        s = "[[" + s.replace(";", "],[") + "]]"
    # Use eval to convert the string to a Python list of lists
    try:
        # yeah it's evil, but we can't use json...
        matrix = eval(s)
    except:
        raise ValueError("Invalid format provided")
    return matrix