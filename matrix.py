class Matrix:
  
  def __init__(self, matrix):

    self.matrix = matrix
    self.m = len(matrix)
    self.n = len(matrix[0])
  
  
  def identity(self, n):
    return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])
  
  def __len__(self):
    return self.m
  
  def __getitem__(self, indices):
    if isinstance(indices, int):  # Single index provided
        return self.matrix[indices]
    elif isinstance(indices, tuple) and len(indices) == 2:  # Two indices provided
        i, j = indices
        return self.matrix[i][j]
    else:
        raise IndexError("Matrix index out of range")
  
  def __str__(self):
    return "[" + ",\n ".join(["[ " + ", ".join(map(str, row)) + " ]" for row in self.matrix]) + "]"
  
  @staticmethod
  def ensure_matrix_format(matrix_obj):
      """Convert input to matrix format if not an instance of the Matrix class."""
      if isinstance(matrix_obj, Matrix):
          return matrix_obj.matrix
      return matrix_obj

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
    
    # Format the display matrix for compact representation
    compact_display = "["
    for i, v in enumerate(display):
        spacer = "[ " if i == 0 else " [ "
        compact_display += spacer + ", ".join(v) + " ],\n"
    compact_display = compact_display.rstrip(",\n") + "]"
    print(compact_display)
    
    return Matrix(C)

  def __eq__(self, other):
      B = self.ensure_matrix_format(other)
      return self.matrix == B

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
        # Compute the inverse for negative powers
        inverse = self.inverse()
        if inverse is None:
            print("Matrix is singular. Cannot compute negative power.")
            return None
        return inverse ** (-power)

    result = self.identity(self.m)
    for _ in range(power):
        result = result * self

    return result

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
        zero_row = all(entry == 0 for entry in row)
        if not zero_row:
            # Find the position of the leading entry (first non-zero element) in the row
            for col, entry in enumerate(row):
                if entry != 0:
                    # The leading entry should be to the right of the previous row's leading entry
                    if col <= leading_entry_col:
                        return False
                    leading_entry_col = col
                    break
        # All non-leading entries below the leading entry should be zero
        for i in range(col + 1, len(row)):
            if row[i] != 0:
                return False
    return True
  
  def is_rref(self):
    """Checks if the matrix is in Reduced Row Echelon Form (RREF)"""
    if not self.is_ref:
        return False
    
    for i, row in enumerate(self.matrix):
        for j, entry in enumerate(row):
            if entry != 0:  # This is a leading entry
                # The leading entry should be 1
                if entry != 1:
                    return False
                # All other entries in the column should be zero
                for k in range(len(self.matrix)):
                    if k != i and self.matrix[k][j] != 0:
                        return False
                break
    return True

  def to_ref(self):
        matrix = self.matrix
        m, n = self.m, self.n

        # Forward elimination to get Row Echelon Form
        for i in range(m):
            max_row = i
            for k in range(i+1, m):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            if max_row != i:
                self.__swap_rows(i, max_row)

            # Check for zero pivot
            if matrix[i][i] == 0:
                continue

            # Normalize pivot row
            pivot = matrix[i][i]
            if pivot != 1:
                self.__row_divide(i, pivot)

            # Eliminate other rows
            for k in range(i+1, m):
                factor = matrix[k][i]
                if factor != 0:
                    self.__row_subtract(k, i, factor)

        print("The matrix in Row Echelon Form (REF) is:")
        print(self)

  def to_rref(self):
      matrix = self.matrix
      m, n = self.m, self.n

      # First convert to REF
      self.to_ref()

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
                  self.__row_subtract(k, i, factor)

      print("The matrix in Reduced Row Echelon Form (RREF) is:")
      print(self)

  def inverse(self):
    if self.is_square:
        print("Matrix is not square. Cannot compute inverse.")
        return None
    
    # Create augmented matrix [A|I]
    identity_matrix = self.identity(self.m)
    augmented_matrix = [[self.matrix[i][j] for j in range(self.n)] + identity_matrix[i] for i in range(self.m)]
    augmented_matrix_obj = Matrix(augmented_matrix)
    
    # Convert to RREF
    augmented_matrix_obj.to_rref()
    
    # Check if the matrix is invertible
    for i in range(self.m):
        if augmented_matrix_obj[i][i] != 1:
            print("Matrix is singular (not invertible).")
            return None
    
    # Extract the inverse from the augmented matrix
    inverse_matrix = [[augmented_matrix_obj[i][j] for j in range(self.n, 2*self.n)] for i in range(self.m)]
    return Matrix(inverse_matrix)

  def free_variables(self):
    # Check for leading 1s
    for i in range(self.m):
      if self.matrix[i][i] != 1:
        return False
    
    # Check for leading 0s
    for i in range(self.m):
      for j in range(self.n):
        if i != j and self.matrix[i][j] != 0:
          return False
    
    return True

  @property
  def is_square(self):
    return self.m == self.n
  
  def is_symmetric(self):
    if not self.is_square:
      return False
    
    for i in range(self.m):
      for j in range(self.n):
        if self.matrix[i][j] != self.matrix[j][i]:
          return False
    
    return True

  def get_num_pivots(self):
    return len(self.pivots())

  def get_pivot_cols(self):
    pivots = []
    for i in range(self.m):
      for j in range(self.n):
        if self.matrix[i][j] == 1:
          pivots.append(j)
          break
    
    return pivots

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
        
        # Forward elimination
        for i in range(m):
            max_row = i
            for k in range(i+1, m):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            if max_row != i:
                self.__swap_rows(i, max_row)
            
            # Check for zero pivot
            if matrix[i][i] == 0:
                break
            
            # Normalize pivot row
            pivot = matrix[i][i]
            if pivot != 1:
                self.__row_divide(i, pivot)
            
            # Eliminate other rows
            for k in range(i+1, m):
                factor = matrix[k][i]
                if factor != 0:
                    self.__row_subtract(k, i, factor)
        
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
  
  def __swap_rows(self, i, j):
        """Swap rows i and j of the matrix."""
        self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
        print("Swapping row {} with row {}: r{}↔r{}".format(i+1, j+1, i+1, j+1))
        print(self)
        
  def __row_divide(self, i, val):
      """Divide row i by the value val."""
      self.matrix[i] = [self.matrix[i][j] / val for j in range(self.n)]
      print("Divide row {} by {}".format(i+1, val))
      print(self)

  def __row_subtract(self, i, j, factor):
      """Subtract factor times row j from row i."""
      for k in range(self.n):
          self.matrix[i][k] -= factor * self.matrix[j][k]
      print("Subtract {} times row {} from row {}".format(factor, j+1, i+1))
      print(self)
  
  
  
  # TODO Implement a proper linear system solver that handles the cases where we need s and t
  
  
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
  #m = matrix.matrix if isinstance(matrix, Matrix) else matrix
  m = len(matrix)
  
  # Check if constants are provided or if augmented matrix is given
  if constants:
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
          formatted_row = " | ".join("{:8.2f}".format(x) for x in row)
          print(formatted_row)
      print('-' * (10 * (n+1)))
  
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
          print("Swapping row {} with row {}: r{}↔r{}".format(i+1, max_row+1, i+1, max_row+1))
          print_matrix(matrix)
      
      # Check for zero pivot, which indicates possible multiple solutions or no solution
      if matrix[i][i] == 0:
          break
      
      # Normalize pivot row
      pivot = matrix[i][i]
      for j in range(n+1):
          matrix[i][j] /= pivot
      print("Normalize row {} with pivot {} by dividing row {} by {}".format(i+1, pivot, i+1, pivot))
      print_matrix(matrix)
      
      # Eliminate other rows
      for k in range(i+1, m):
          factor = matrix[k][i]
          print("Eliminate below pivot in column {} by subtracting {} * row {} from row {}".format(i+1, factor, i+1, k+1))
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