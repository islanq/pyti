
class Symbol:
    _globals = {}  # Class variable to store global symbols
    
    def __init__(self, name):
        """Initialize a Symbol instance and store it in the global symbols dictionary."""
        if not isinstance(name, str):
            raise TypeError("Symbol name should be a string.")
        self.name = name
        Symbol._globals[name] = self

    def __repr__(self):
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
    def __add__(self, other):
        if isinstance(other, (Symbol, int, float)):
            return Symbol(self.name + " + " + str(other))

    def __radd__(self, other):
            return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (Symbol, int, float)):
            return Symbol(self.name + " - " + str(other))

    def __rsub__(self, other):
            return self.__sub__(other)
   
    def __mul__(self, other):
        if isinstance(other, Symbol):
            return Symbol(self.name + " * " + str(other))
        if isinstance(other, (int, float)):
            return Symbol(str(other) + " * " + self.name)
        
    def __rmul__(self, other):
        if isinstance(other, (Symbol, int, float)):
            return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (Symbol, int, float)):
            return Symbol(self.name + " / " + str(other))

        
    def __rtruedive__(self, other):
        return self.__truediv__(other)
    
    def __pow__(self, other):
        if isinstance(other, (Symbol, int, float)):
            return Symbol(self.name + " ^ " + str(other))
    
    def __rpow__(self, other):
        return self.__pow__(other)

    @classmethod
    def set_globals(cls, _globals=None):
        """Set the global symbols dictionary."""
        cls._globals = _globals if _globals is not None else {}
    
    @classmethod
    def clear(cls):
        """Clear all Symbols from the global symbols dictionary."""
        cls._globals.clear()
    
    @classmethod
    def list(cls):
        """List all Symbols in the global symbols dictionary."""
        return list(cls._globals.keys())
    
    @classmethod
    def remove(cls, symbol):
        """Remove a Symbol from the global symbols dictionary."""
        if isinstance(symbol, Symbol):
            symbol = symbol.name
        
        if symbol in cls._globals:
            del cls._globals[symbol]
        else:
            print("Symbol {} does not exist.".format(symbol))
    
    @classmethod
    def add(cls, symbol_str):
        """Add one or multiple Symbols to the global symbols dictionary."""
        if not isinstance(symbol_str, str):
            raise TypeError("Expected a string of symbol names.")
        
        for symbol_name in symbol_str.split():
            cls._globals[symbol_name] = cls(symbol_name)

        
def symbols(names: str):
    Symbol.add(names)
    return tuple(Symbol._globals[name] for name in names.split())

# Your helper function that returns a list of variable names
def get_vars_from_expression(expression):
    from math_parsing import parse_variables
    return parse_variables(expression)

# Function to dynamically create Symbol objects
def create_dynamic_symbols(variable_names):
    Symbol.add(" ".join(variable_names))
    for name in variable_names:
        try:
            # Dynamically create Python variables and assign Symbol objects to them
            exec("global {}; {} = Symbol._globals['{}']".format(name, name, name))
        except Exception as e:
            print("Error creating Symbol object for variable {}.".format(name))
            print(e)
            continue
