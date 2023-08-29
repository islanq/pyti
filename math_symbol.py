# Add back the missing arithmetic operation methods to the Symbol class
from collections import namedtuple
from math_expression import Expression
# Define a named tuple for holding polynomial information
PolyInfo = namedtuple('PolyInfo', ['degree', 'coeffs'])

class SymbolTable:
    def __init__(self):
        self.table = {}
        
    def add_symbol(self, name, value=None):
        symbol = Symbol(name, value)
        self.table[name] = symbol
        return symbol
    
    def get_symbol(self, name):
        return self.table.get(name, None)
    
    def remove_symbol(self, name):
        if name in self.table:
            del self.table[name]
            
    def clear_all(self):
        self.table.clear()

class Symbol:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.history = []
        self.poly_info = PolyInfo(degree=0, coeffs={0: 1})  # x to the power of 0 is 1

    def clone(self):
        new_symbol = Symbol(self.name, self.value)
        new_symbol.history = self.history.copy()
        new_symbol.poly_info = PolyInfo(self.poly_info.degree, self.poly_info.coeffs.copy())
        return new_symbol

    def __add__(self, other):
        if isinstance(other, (Expression, Symbol)):
            other = other.symbol if isinstance(other, Expression) else other
        new_symbol = self.clone()
        new_symbol.history.append(('add', other))
        new_coeffs = new_symbol.poly_info.coeffs.copy()
        new_coeffs[0] = new_coeffs.get(0, 0) + (other if isinstance(other, int) else 1)
        new_symbol.poly_info = PolyInfo(degree=new_symbol.poly_info.degree, coeffs=new_coeffs)
        return Expression(new_symbol, symbols=[self, other] if isinstance(other, Symbol) else [self])

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, (Expression, Symbol)):
            other = other.symbol if isinstance(other, Expression) else other
        new_symbol = self.clone()
        new_symbol.history.append(('mul', other))
        factor = other if isinstance(other, int) else 1
        new_coeffs = {k: v * factor for k, v in new_symbol.poly_info.coeffs.items()}
        new_symbol.poly_info = PolyInfo(degree=new_symbol.poly_info.degree, coeffs=new_coeffs)
        return Expression(new_symbol, symbols=[self, other] if isinstance(other, Symbol) else [self])

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __sub__(self, other):
        if isinstance(other, (Expression, Symbol)):
            other = other.symbol if isinstance(other, Expression) else other
        new_symbol = self.clone()
        new_symbol.history.append(('sub', other))
        new_coeffs = new_symbol.poly_info.coeffs.copy()
        new_coeffs[0] = new_coeffs.get(0, 0) - (other if isinstance(other, int) else 1)
        new_symbol.poly_info = PolyInfo(degree=new_symbol.poly_info.degree, coeffs=new_coeffs)
        return Expression(new_symbol, symbols=[self, other] if isinstance(other, Symbol) else [self])

    def __rsub__(self, other):
        return self.__sub__(other)


    def __truediv__(self, other):
        if isinstance(other, Expression):
            other = other.symbol
        new_symbol = self.clone()
        new_symbol.history.append(('div', other))
        new_coeffs = {k: v / 1 for k, v in new_symbol.poly_info.coeffs.items()}  # Update coeffs
        new_symbol.poly_info = PolyInfo(degree=new_symbol.poly_info.degree, coeffs=new_coeffs)
        return Expression(new_symbol)
    
    def __rtruediv__(self, other):
        return self.__truediv__(other)
    
    def __pow__(self, other):
        if isinstance(other, Expression):
            other = other.symbol
        new_symbol = self.clone()
        new_symbol.history.append(('pow', other))
        new_degree = max(new_symbol.poly_info.degree, 1)
        new_coeffs = {1: 1}  # Assuming we start from x, this is a simplified approach
        new_symbol.poly_info = PolyInfo(degree=new_degree, coeffs=new_coeffs)
        return Expression(new_symbol)
    
    def __rpow__(self, other):
        return self.__pow__(other)
    
    def __repr__(self):
        return self.name

# Initialize Symbol with a value and then perform some operations
"""
x = Symbol('x',.2)
expr = x ** 2  # Power
expr = expr * 3  # Multiply
expr = expr + 2  # Add
expr = expr - 1  # Subtract
expr = expr / 2  # Divide

# Get polynomial information
expr.symbol.poly_info.degree, expr.symbol.poly_info.coeffs
print(expr.symbol.poly_info.degree, expr.symbol.poly_info.coeffs)
"""