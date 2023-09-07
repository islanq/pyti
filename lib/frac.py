from collections import namedtuple
FracTuple = namedtuple('FracTuple', ['numerator', 'denominator'])

class Frac:

    def __init__(self, num, error=0.000001) -> None:
        self._error = error
        
        if isinstance(num, Frac):
            self._n = num.numerator
            self._d = num.denominator
        
        elif isinstance(num, int):
            self._n = num
            self._d = 1
        
        elif isinstance(num, float):
            self._n, self._d = self.dec_to_frac(num, error)
            
        elif self._is_frac_tuple(num):
            self._n = num[0]
            self._d = num[1]    
        
        elif isinstance(num, str):
            if num.count('.') == 1:
                num = float(num)
            elif num.count('/') == 1:
                n, d = num.split('/')
                num = float(n) / float(d)
            else:
                try:
                    num = float(eval(num))
                except:
                    raise ValueError("Invalid string representation of a fraction.")
                    
            self._n, self._d = self.dec_to_frac(float(num), error)
            
        elif isinstance(num, complex):
            raise ValueError("Complex numbers cannot be directly represented as a fraction.")
        else:
            raise TypeError("Unsupported type for Fraction.")
        if (self._d == 0):
            raise ZeroDivisionError("The denominator cannot be 0!")
            
        self._dec = self._n / self._d

    @staticmethod
    def dec_to_frac(x, error = 0.000001):
        if isinstance(x, Frac):
            return x
        
        n = int(x // 1)
        x -= n
        
        if x < error:
            return (n, 1)
        elif 1 - error < x:
            return (n + 1, 1)
        
        lower_n = 0
        lower_d = 1
        upper_n = 1
        upper_d = 1
        
        while True:
            middle_n = lower_n + upper_n
            middle_d = lower_d + upper_d
            if middle_d * (x + error) < middle_n:
                upper_n = middle_n
                upper_d = middle_d
            elif middle_n < (x - error) * middle_d:
                lower_n = middle_n
                lower_d = middle_d
            else:
                return FracTuple(n * middle_d + middle_n, middle_d)
    
    @property
    def approx(self):
        return float(self._dec)
    
    @property
    def numerator(self) -> int:
        return self._n
    
    @property
    def denominator(self) -> int:
        return self._d
    
    @property
    def n(self) -> int:
        return self.numerator
    
    @property
    def d(self) -> int:
        return self.denominator
    
    def __float__(self) -> float:
        try:
            return float(self.n/self.d)
        except Exception as e:
            print("There was an error casting to float {}".format(e))
            print("attempting to return {}".format(self.approx))
            return self.approx
        finally:
            return self.approx
    
    def __int__(self) -> int:
        return int(self.approx)
    
    def __str__(self) -> str:
       return "{}/{}".format(self.n, self.d) if self.approx != int(self) else str(int(self))
    
    def __tuple__(self) -> tuple:
        return (self.n, self.d)
    
    def to_dict(self) -> dict:
        return {
            'numerator': self.n,
            'denominator': self.d
        }
    
    def __repr__(self):
        return "{}/{}".format(self.n, self.d) if self.approx != int(self) else str(int(self))
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self._n * other._d + other._n * self._d
        new_d = self._d * other._d
        return Frac(new_n / new_d)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __iadd__(self, other):
        result = self + other
        self._n, self._d = result.n, result.d
        return self

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self._n * other._d - other._n * self._d
        new_d = self._d * other._d
        return Frac(new_n / new_d)
    
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __isub__(self, other):
        result = self - other
        self._n, self._d = result.n, result.d
        return self
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self._n * other._n
        new_d = self._d * other._d
        return Frac(new_n / new_d)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __imul__(self, other):
        result = self * other
        self._n, self._d = result.n, result.d
        return self
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self._n * other._d
        new_d = self._d * other._n
        return Frac(new_n / new_d)
    
    def __rtruediv__(self, other):
        return self.__truediv__(other)
    
    def __idiv__(self, other):
        result = self / other
        self._n, self._d = result.n, result.d
        return self
    
    def __floordiv__(self, other):
        if isinstance(other, (int, float, Frac)):
            other = Frac(other)
        result = self._n * other._d // (self._d * other._n)
        return Frac(result)
    
    def _is_frac_tuple(self, other) -> bool:
        if not isinstance(other, tuple):
            return False
        if not len(other) == 2:
            return False
        return all(isinstance(t, int) for t in other) and other[1] != 0

    def _to_fraction(self, other):
        if isinstance(other, Frac):
            return other
        elif isinstance(other, (int, float, tuple)):
            return Frac(other)
        else:
            return None

    def __eq__(self, other) -> bool:
        other = self._to_fraction(other)
        if other is not None:
            return self._n * other._d == self._d * other._n
        return False

    def __ne__(self, other) -> bool :
        return not self.__eq__(other)

    def __gt__(self, other) -> bool:
        other = self._to_fraction(other)
        if other is not None:
            return self._n * other._d > self._d * other._n
        return False

    def __ge__(self, other) -> bool:
        other = self._to_fraction(other)
        if other is not None:
            return self.__eq__(other) or self.__gt__(other)
        return False

    def __lt__(self, other) -> bool:
        other = self._to_fraction(other)
        if other is not None:
            return not self.__eq__(other) and not self.__gt__(other)
        return False

    def __le__(self, other: ('Frac', int, float)) -> bool:
        other = self._to_fraction(other)
        if other is not None:
            return self.__eq__(other) or self.__lt__(other)
        return False
    
    def __iter__(self):
        yield self.n
        yield self.d

