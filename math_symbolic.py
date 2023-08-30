from collections import namedtuple

from math_parsing import parse_expression, parse_variables

PolyInfo = namedtuple('PolyInfo', ['degree', 'coeffs'])

class GlobalSymbolTable:
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
        self.poly_info = PolyInfo(degree=1 if name else 0, coeffs={0: 0, 1: 1 if name else 0})  # x to the power of 0 is 1

    def clone(self):
        new_symbol = Symbol(self.name, self.value)
        new_symbol.history = self.history.copy()
        new_symbol.poly_info = PolyInfo(self.poly_info.degree, self.poly_info.coeffs.copy())
        return new_symbol

    def __add__(self, other):
        if isinstance(other, Expression):
            other = other.symbol
        new_symbol = self.clone()
        new_symbol.history.append(('add', other))
        
        new_coeffs = new_symbol.poly_info.coeffs.copy()
        new_coeffs[0] = new_coeffs.get(0, 0) + (other if isinstance(other, (int, float)) else 0)
        new_coeffs[1] = new_coeffs.get(1, 0) + (1 if isinstance(other, Symbol) and other.name == self.name else 0)
        new_symbol.poly_info = PolyInfo(degree=max(new_symbol.poly_info.degree, 1), coeffs=new_coeffs)
        
        return new_symbol
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        if isinstance(other, Expression):
            other = other.symbol
        new_symbol = self.clone()
        new_symbol.history.append(('mul', other))
        
        new_coeffs = {k: v * (other if isinstance(other, (int, float)) else 1) for k, v in new_symbol.poly_info.coeffs.items()}
        new_symbol.poly_info = PolyInfo(degree=new_symbol.poly_info.degree, coeffs=new_coeffs)
        
        return new_symbol
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        if isinstance(other, Expression):
            other = other.symbol
        new_symbol = self.clone()
        new_symbol.history.append(('sub', other))
        
        new_coeffs = new_symbol.poly_info.coeffs.copy()
        new_coeffs[0] = new_coeffs.get(0, 0) - (other if isinstance(other, (int, float)) else 0)
        new_symbol.poly_info = PolyInfo(degree=max(new_symbol.poly_info.degree, 1), coeffs=new_coeffs)
        
        return new_symbol
    
    def __rsub__(self, other):
        return self.__sub__(other)

    def __truediv__(self, other):
        if isinstance(other, Expression):
            other = other.symbol
        new_symbol = self.clone()
        new_symbol.history.append(('div', other))
        
        new_coeffs = {k: v / (other if isinstance(other, (int, float)) else 1) for k, v in new_symbol.poly_info.coeffs.items()}
        new_symbol.poly_info = PolyInfo(degree=new_symbol.poly_info.degree, coeffs=new_coeffs)
        
        return new_symbol

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __pow__(self, other):
        if isinstance(other, Expression):
            other = other.symbol
        new_symbol = self.clone()
        new_symbol.history.append(('pow', other))
        
        new_degree = new_symbol.poly_info.degree * (other if isinstance(other, (int, float)) else 1)
        new_coeffs = {k * (other if isinstance(other, (int, float)) else 1): v for k, v in new_symbol.poly_info.coeffs.items()}
        new_symbol.poly_info = PolyInfo(degree=new_degree, coeffs=new_coeffs)
        
        return new_symbol
        
    def __rpow__(self, other):
        return self.__pow__(other)

    def __repr__(self):
        return self.name

    def to_expression(self):
        return Expression(self)
    
global_symbol_table = GlobalSymbolTable()
# Correcting the Expression class to wrap the new Symbol object properly
class Expression:

    def __init__(self, symbol_or_expression, symbols=[]):
        if isinstance(symbol_or_expression, str):
            # If a string expression is passed, parse it
            parsed_expression = parse_expression(symbol_or_expression)
            variables = parse_variables(symbol_or_expression)
            
            # Dynamically add these variables to the global symbol table if they are not already there
            for variable in variables:
                if global_symbol_table.get_symbol(variable) is None:
                    global_symbol_table.add_symbol(variable)
            
            self.symbol = Symbol(parsed_expression)
            self.symbols = variables
        else:
            self.symbol = symbol_or_expression
            self.symbols = symbols
        
    def get_symbol(self, name) -> Symbol:
        return global_symbol_table.get_symbol(name)

    def __add__(self, other):
        new_symbol = self.symbol.__add__(other)
        return Expression(new_symbol.symbol if isinstance(new_symbol, Expression) else new_symbol)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        new_symbol = self.symbol.__sub__(other)
        return Expression(new_symbol.symbol if isinstance(new_symbol, Expression) else new_symbol)
    
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __mul__(self, other):
        new_symbol = self.symbol.__mul__(other)
        return Expression(new_symbol.symbol if isinstance(new_symbol, Expression) else new_symbol)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        new_symbol = self.symbol.__truediv__(other)
        return Expression(new_symbol.symbol if isinstance(new_symbol, Expression) else new_symbol)
    
    def __rtruediv__(self, other):
        return self.__truediv__(other)
    
    def __pow__(self, other):
        new_symbol = self.symbol.__pow__(other)
        return Expression(new_symbol.symbol if isinstance(new_symbol, Expression) else new_symbol)
    
    def __rpow__(self, other):
        return self.__pow__(other)
    
    def get_alt_poly_coeffs(self):
        coeffs = self.symbol.poly_info.coeffs
        alt_coeffs = [0, 0]  # Initialize with zeros: [variable_coeff, constant_term]
        
        # Variable coefficient
        alt_coeffs[0] = coeffs.get(1, 0)
        
        # Constant term
        alt_coeffs[1] = coeffs.get(0, 0)
        
        return alt_coeffs
    
    def __repr__(self):
        terms = []
        factors = [self.symbol.name]  # Initialize with the symbol itself
        for op, operand in self.symbol.history:
            if op in ['add', 'sub']:
                if factors:
                    terms.append(' * '.join(factors))
                    factors = [self.symbol.name]
                if op == 'add':
                    terms.append("+ {}".format(operand))
                else:
                    terms.append("- {}".format(operand))
            elif op == 'mul':
                factors.append(str(operand))
            elif op == 'div':
                factors[-1] = f"{factors[-1]} / {operand}"
            elif op == 'pow':
                factors[-1] = f"{factors[-1]} ^ {operand}"
        
        if factors:
            terms.append(' * '.join(factors))

        return ' '.join(terms).lstrip('+ ')
    
    
# Debugging: Let's print the internal variables at each step to identify the issue
# h = Symbol('h')
# e1 = Expression(h)
# result1 = e1.get_alt_poly_coeffs()

# e2 = e1 + (-2)
# result2 = e2.get_alt_poly_coeffs()

# e3 = (e1 + 5) + h  # Using `h` directly here instead of 3 * h
# result3 = e3.get_alt_poly_coeffs()

# result1, result2, result3

# print(result1, result2, result3)

h = Symbol('h')   

e1 = h
result1 = Expression(e1).get_alt_poly_coeffs()
print(f"Alt Poly Coeffs of e1 (h): {result1}")

# Test 2: polyCoeffs(h-2) should be [1, -2]
e2 = h + (-2)  # Using +(-2) instead of -(2) to trigger the __add__ method
result2 = Expression(e2).get_alt_poly_coeffs()
print(f"Alt Poly Coeffs of e2 (h-2): {result2}")

# Test 3: polyCoeffs(3*h+5) should be [3, 5]
e3 = 3 * h + 5  # Using multiplication and addition to test
result3 = Expression(e3).get_alt_poly_coeffs()
print(f"Alt Poly Coeffs of e3 (3*h+5): {result3}")


e4 = Expression('3*h+5x')
print(e4.get_symbol('x'))
print(e4.get_symbol('h').to_expression().get_alt_poly_coeffs())