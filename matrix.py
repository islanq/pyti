from matrix_format import FormatterTemplate
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
    return self.template.format_matrix(self.matrix)
  
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
  
  def is_ref(self):
    """Checks if the matrix is in Row Echelon Form (REF)"""
    leading_entry_col = -1
    for row in self.matrix:
        first_nonzero_col = next((index for index, entry in enumerate(row) if entry != 0), -1)
        
        # If the row is all zeros, continue to the next row
        if first_nonzero_col == -1:
            continue
        
        # Check if leading entry is to the right of the previous row's leading entry
        if first_nonzero_col <= leading_entry_col:
            return False
        
        leading_entry_col = first_nonzero_col
        
        # Check if all entries to the right of the leading entry are zeros
        if any(row[first_nonzero_col+1:]):
            return False
    return True
  
  def is_rref(self):
    """Checks if the matrix is in Reduced Row Echelon Form (RREF)"""
    if not self.is_ref():
        return False
    for i, row in enumerate(self.matrix):
        for j, entry in enumerate(row):
            if entry == 1:  # This is a leading entry
                # All other entries in the column should be zero
                if any(row[:j]) or any(row[j+1:]) or any(row[j] for idx, row in enumerate(self.matrix) if idx != i):
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
      if self.is_rref:
          print("Matrix is already in RREF.")
          return
        
      matrix = self.matrix
      m, n = self.m, self.n

      # First convert to REF
      self.to_ref(True)

      # Backward elimination to get Reduced Row Echelon Form
      for i in range(m - 1, -1, -1):
          # Find the pivot column
          pivot_col = None
          for j in range(n):
              if matrix[i][j] != 0:
                  pivot_col = j
                  break

          # If no pivot column is found, move to next row
          if pivot_col is None:
              continue

          # Eliminate entries above the pivot
          for k in range(i - 1, -1, -1):
              factor = matrix[k][pivot_col]
              if factor != 0:
                  self._row_subtract(k, i, factor)
                  
      print("The matrix in Reduced Row Echelon Form (RREF) is:")
      self.pm.add_to_queue(self.template.format_matrix(self.matrix))

  def inverse(self):
    if not self.is_square:
        print("Matrix is not square. Cannot compute inverse.")
        return None
    # Create augmented matrix [A|I] and convert to RREF
    identity_matrix = self.identity(self.m)
    augmented_matrix = [row + identity_row for row, identity_row in zip(self.matrix, identity_matrix)]
    augmented_matrix_obj = Matrix(augmented_matrix)
    augmented_matrix_obj.to_rref()
    # Check if the matrix is invertible
    if not all(augmented_matrix_obj[i][i] == 1 for i in range(self.m)):
        print("Matrix is singular (not invertible).")
        return None
    # Extract the inverse from the augmented matrix
    return Matrix([row[self.n:] for row in augmented_matrix_obj.matrix])

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

  def determinant(self):
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
      return
      if display:
        operation_display = self.template.format_operation('swap', i, j)
        matrix_display = self.template.format_matrix(self.matrix)
        self.pm.add_to_queue(operation_display + "\n" + matrix_display)

  def _row_divide(self, i, val, display=True):
      """Divide row i by the value val."""
      if val == 0 or val is None:
        return
      
      self.matrix[i] = [self.matrix[i][j] / val for j in range(self.n)]
      print("R{} ← R{} / {}".format(i+1, i+1, val))
      print(" " + str(self.get_row(i)))
      return

      if display:
        operation_display = self.template.format_operation('mul', i, val)
        matrix_display = self.template.format_matrix(self.matrix)
        self.pm.add_to_queue(operation_display + "\n" + matrix_display)
        print("\n" + str(self.get_row(i+1)) + "\n")

  def _row_multiply(self, i, val, display=True):
      """Multiply row i by the value val."""
      self.matrix[i] = [self.matrix[i][j] * val for j in range(self.n)]
      print("R{} ← R{} * {}".format(i+1, i+1, val))
      return
      if display:
        operation_display = self.template.format_operation('div', i, val)
        matrix_display = self.template.format_matrix(self.matrix)
        self.pm.add_to_queue(operation_display + "\n" + matrix_display)
      
  def _row_subtract(self, i, j, factor=1, display=True):
      """Subtract factor times row j from row i."""
      if factor is None:
        return
      self.matrix[i] = [self.matrix[i][k] - factor * self.matrix[j][k] for k in range(self.n)]
      #for k in range(self.n):
     #     self.matrix[i][k] -= factor * self.matrix[j][k]
      print("R{} ← R{} - ({} * R{})".format(i+1, i+1, factor, j+1))
      print(" " + str(self.get_row(i)))
      return
      
      if display:
        operation_display = self.template.format_operation('sub', i, j, factor)
        matrix_display = self.template.format_matrix(self.matrix)
        self.pm.add_to_queue(operation_display + "\n" + matrix_display)
        

  def _row_add(self, i, j, factor=1, display=True):
    """Add factor times row j to row i."""
    self.matrix[i] = [self.matrix[i][k] + factor * self.matrix[j][k] for k in range(self.n)]

#    for k in range(self.n):
 #       self.matrix[i][k] += factor * self.matrix[j][k]
    print("R{} ← R{} + ({} * R{})".format(i+1, i+1, factor, j+1))
    return
    if display:
      operation_display = self.template.format_operation('add', i, j, factor)
      matrix_display = self.template.format_matrix(self.matrix)
      self.pm.add_to_queue(operation_display + "\n" + matrix_display)
  
  def solutions(self):
    """Return the solutions to the system of equations."""
    if not self.is_rref:
      print("Matrix must be in RREF to compute solutions.")
      return None
    
    # Check for no solution or multiple solutions
    for i in range(self.m):
      if all([cell == 0 for cell in self.matrix[i][:-1]]) and self.matrix[i][-1] != 0:
        print("The system has no solution.")
        return None
      if all([cell == 0 for cell in self.matrix[i]]):
        print("The system has infinitely many solutions.")
        return None
    
    # Back-substitution to get the solution
    x = [0 for _ in range(self.n)]
    for i in range(self.m-1, -1, -1):
      x[i] = self.matrix[i][-1]
      for j in range(i+1, self.n):
        x[i] -= self.matrix[i][j] * x[j]
      print("Back substitution for x_{}".format(i+1))
      print("x[{}] = {}".format(i+1, x[i]))
    
    return x
      
  # Row getter and setter methods
  

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

  # TODO Implement a proper linear system solver that handles the cases where we need s and t

def flatten(lst):
    """Flatten a list of lists into a single list."""
    return [item for sublist in lst for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]



def parse_equation_systems(*args):
  parsed_results = []
  variables = []
  
  # Determine the source of equations
  if isinstance(args[0], list) and isinstance(args[0][0], list):  # A list of lists
      equations = [eq[0] for eq in args[0]]
  else:
      equations = args
  
  # Extract unique variables from all equations
  for equation in equations:
      # Remove multiplication symbol
      equation = equation.replace("*", "")
      
      prev_char = ''
      for char in equation:
          if (97 <= ord(char) <= 122) and char not in variables:  # ASCII range for lowercase letters
              # Check if previous character is not an alphabet (to handle functions like sin(x))
              if not prev_char or not (97 <= ord(prev_char) <= 122):
                  variables.append(char)
          prev_char = char
    # Helper function to extract coefficient
  def extract_coefficient(term, var):
      term = term.replace("−", "-")  # Replace the special minus with the regular one
      if term == var:  # e.g. x
          return 1
      elif term == "-" + var:  # e.g. -x
          return -1
      elif term == "+" + var:  # e.g. +x
          return 1
      else:  # e.g. 2x or -2x
          term_val = term.replace(var, "").strip()
          return int(term_val) if term_val not in ["+", "-"] else (1 if term_val == "+" else -1)
  
  for equation in equations:
      equation = equation.replace("−", "-").replace("*", "")  # Replace special minus sign and multiplication symbol
      
      # Split equation to separate LHS and RHS
      lhs, rhs = equation.split("=")
      
      # Use a list comprehension combined with join to split terms better
      terms = ''.join([' ' + i if i in ['+', '-'] else i for i in lhs]).split()
      const = int(rhs.strip())  # Get the constant
      
      # Initialize coefficients as 0 for all variables
      coeffs = [0 for _ in variables]
      
      for term in terms:
          for var in variables:
              if var in term:
                  idx = variables.index(var)
                  coeffs[idx] += extract_coefficient(term, var)
                  
      coeffs.append(const)                
      parsed_results.append(coeffs)
  
  return parsed_results

def matrix_multiply_compact(A, B):
  # Check if matrices can be multiplied
  if len(A[0]) != len(B):
    return "Matrices cannot be multiplied"
  
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
  
  # Format the display matrix for compact representation
  compact_display = "[\n"
  for row in display:
    compact_display += "[ " + ", ".join(row) + "],\n"
  compact_display += "]"
  
  print(compact_display)
  
  return C

def gaussian_elimination(matrix, constants=None):
    m = len(matrix)
    
    # Check if constants are provided or if augmented matrix is given
    if isinstance(constants, bool) and constants == True:
        n = len(matrix[0]) - 1
    elif isinstance(constants, list):
        n = len(matrix[0])
        for i in range(m):
            matrix[i].append(constants[i])
    else:
        user_input = input("Is the augmented part included in the matrix (yes/no)? ").strip().lower()
        if user_input == "yes":
            n = len(matrix[0]) - 1
        elif user_input == "no":
            print("Please provide the matrix in the augmented form.")
            return None
        else:
            print("Invalid input. Please provide either 'yes' or 'no'.")
            return None
  
    def print_matrix(matrix):
        for row in matrix:
            formatted_row = " | ".join("{:6.2f}".format(x) for x in row)
            print(formatted_row)
        print('-' * len(formatted_row) + 2*'-')
  
    for i in range(m):
        # Find pivot element and swap rows if necessary
        max_val = abs(matrix[i][i])
        max_row = i
        for k in range(i+1, m):
            if abs(matrix[k][i]) > max_val:
                max_val = abs(matrix[k][i])
                max_row = k
        if i != max_row:
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            print("r{}↔r{}".format(i+1, max_row+1))
            print_matrix(matrix)
        
        # Check for zero pivot, which indicates possible multiple solutions or no solution
        if matrix[i][i] == 0:
            break

        # Normalize pivot row
        pivot = matrix[i][i]
        for j in range(n+1):
            matrix[i][j] /= pivot
        print("R{} = R{}/{}".format(i+1, i+1, pivot))
        print_matrix(matrix)

        # Eliminate other rows
        for k in range(i+1, m):
            factor = matrix[k][i]
            print("R{} = R{}-R{}*{}".format(k+1, k+1, i+1, factor))
            for j in range(n+1):
                matrix[k][j] -= factor * matrix[i][j]
            print_matrix(matrix)

    # Check for no solution or multiple solutions
    for i in range(m):
        if all([cell == 0 for cell in matrix[i][:-1]]) and matrix[i][-1] != 0:
            print("The system has no solution.")
            return None
        if all([cell == 0 for cell in matrix[i]]):
            print("The system has infinitely many solutions.")
            return None

    # Back-substitution to get the solution
    x = [0 for _ in range(n)]
    for i in range(m-1, -1, -1):
        x[i] = matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= matrix[i][j] * x[j]
        print("Back substitution for x_{}".format(i+1))
        print("x[{}] = {}".format(i+1, x[i]))

    return x



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
  
