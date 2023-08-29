# Update the Expression class to support arithmetic operations

class Expression:
    def __init__(self, symbol, symbols=[]):
        self.symbol = symbol
        self.symbols = symbols

    def __add__(self, other):
        return self.symbol.__add__(other)
    
    def __sub__(self, other):
        return self.symbol.__sub__(other)
    
    def __mul__(self, other):
        return self.symbol.__mul__(other)
    
    def __truediv__(self, other):
        return self.symbol.__truediv__(other)
    
    def __pow__(self, other):
        return self.symbol.__pow__(other)

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