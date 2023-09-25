from collections import namedtuple
FracTuple = namedtuple('FracTuple', ['numerator', 'denominator'])


class Frac:

    def __init__(self,
                 number: int | float | FracTuple | Frac | str = 0,
                 denom: int = 1,
                 error=1e-6) -> None:
        
        self._num = None
        self._den = None
        self._dec = None
        self._error = error
        self._refresh = True
        
        if isinstance(number, (int, float)):
            self.n, self.d = (number, denom or 1)
        elif isinstance(number, (Frac, FracTuple)):
            self.n, self.d = (number.numerator, number.denominator)
        elif isinstance(number, str):
            self.n, self.d = self._parse_from_string(number)
        else:
            raise TypeError("Invalid type for number: {}".format(type(number)))
            
        if denom == 1:
            self._n, self._d = self.dec_to_frac(self.approx, error=error)
    #region Getters
    @property
    def approx(self) -> float:
        self._update()
        return float(self._dec)

    @property
    def numerator(self) -> int | float:
        self._update()
        return self._num

    @property
    def denominator(self) -> int | float:
        self._update()
        return self._den
    
    @property
    def n(self) -> int | float:
        return self.numerator

    @property
    def d(self) -> int | float:
        return self.denominator

    #endregion Getters

    #region Setters

    @n.setter
    def n(self, numerator) -> None:
        self.numerator = numerator
        
    @d.setter
    def d(self, denominator) -> None:
        self.denominator =  denominator
    
    @denominator.setter
    def denominator(self, denominator: int | float) -> None:
        if denominator == 0:
            raise ZeroDivisionError("The denominator cannot be 0!")
        denominator = self._reduce_if_possible(denominator)
        if self._den != denominator:
            self._den = denominator
            self._refresh = True
        
    @numerator.setter
    def numerator(self, numerator: int) -> None:
        numerator = self._reduce_if_possible(numerator)
        if self._num != numerator:
            self._num = numerator
            self._refresh = True
        
    #endregion Setters
        
    #endregion Properties
    def proper(self) -> str:
        integer = int(self)
        fraction = self % integer
        
        return "{}{}{}".format(integer, '' if fraction < 0 else '+', fraction)
        
    @staticmethod
    def dec_to_frac(x, error=1e-6) -> FracTuple:
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
                return FracTuple(int(n * middle_d + middle_n), (middle_d))

    def _reduce_if_possible(self, decimal: float) -> int | float:
        integer = int(decimal)
        return integer if integer == decimal else decimal

    def _update(self) -> None:
        if not self._refresh:
            return
        
        self._dec = self._num / self._den
        self._num, self._den = self.dec_to_frac(self._dec, error=self._error)
        self._num = abs(self._num)
        self._den = abs(self._den)
        if self._dec < 0:
            self._num *= -1
        self._refresh = False
    
    def _is_frac_tuple(self, other) -> bool:
        if not isinstance(other, tuple):
            return False
        if not len(other) == 2:
            return False
        return all(isinstance(t, int) for t in other) and other[1] != 0

    def _to_fraction(self, other) -> Frac:
        if isinstance(other, Frac):
            return other
        elif isinstance(other, (int, float, tuple)):
            return Frac(other)
        elif 'fractions' in sys.modules:
            if isinstance(other, Fraction):
                return Frac(other.numerator, other.denominator)
            return None

    def _parse_from_string(self, string: str):
        string = string.strip().replace(' ', '')

        if string.count('/') == 1:
            try:
                num, den = string.split('/')
                num = eval(num)
                den = eval(den)
                num = self._reduce_if_possible(float(num))
                den = self._reduce_if_possible(float(den))
                return num, den
            except:
                pass
        else:
            try:
                num = eval(string)
                num = self._reduce_if_possible(float(num))
                return num, 1
            except:
                pass
        raise ValueError("Invalid string for Frac: {}".format(string))

    def __getitem__(self, key: int) -> int:
        if key not in (0, 1): raise IndexError("Frac only has two elements.")
        if   key == 0: return self.n
        elif key == 1: return self.d
     
    def __setitem__(self, key: int, value: int) -> None:
        if key not in (0, 1): raise IndexError("Frac only has two elements.")
        if    key == 0: self.n = value
        elif  key == 1: self.d = value

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

    def __tuple__(self) -> tuple:
        return FracTuple(self.n, self.d)

    def __set__(self) -> set:
        return {self.n, self.d}

    def __list__(self) -> list:
        return [self.n, self.d]
    
    def __str__(self) -> str:
    
    def __Fraction__(self) -> 'Fraction':
        return Fraction(self.n, self.d)
    
    #region Arithmetic operators

    def __add__(self, other) -> Frac:
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self.n * other.d + other.n * self.d
        new_d = self.d * other.d
        return Frac(new_n / new_d)

    def __radd__(self, other) -> Frac:
        return self.__add__(other)

    def __iadd__(self, other) -> Frac:
        result = self + other
        self.n, self.d = result.n, result.d
        return self

    def __sub__(self, other) -> Frac:
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self.n * other.d - other.n * self.d
        new_d = self.d * other.d
        return Frac(new_n / new_d)

    def __rsub__(self, other) -> Frac:
        return self.__sub__(other)

    def __isub__(self, other) -> Frac:
        result = self - other
        self.n, self.d = result.n, result.d
        return self

    def __mul__(self, other) -> Frac:
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self.n * other.n
        new_d = self.d * other.d
        return Frac(new_n / new_d)

    def __rmul__(self, other) -> Frac:
        return self.__mul__(other)

    def __imul__(self, other) -> Frac:
        result = self * other
        self.n, self.d = result.n, result.d
        return self

    def __truediv__(self, other) -> Frac:
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self.n * other.d
        new_d = self.d * other.n
        return Frac(new_n / new_d)

    def __rtruediv__(self, other) -> Frac:
        return self.__truediv__(other)

    def __idiv__(self, other) -> Frac:
        result = self / other
        self.n, self.d = result.n, result.d
        return self

    def __floordiv__(self, other) -> Frac:
        if isinstance(other, (int, float, Frac)):
            other = Frac(other)
        result = self.n * other.d // (self.d * other.n)
        return Frac(result)
    
    def __rfloordiv__(self, other) -> Frac:
        return self.__floordiv__(other)
    
    def __ifloordiv__(self, other) -> Frac:
        result = self // other
        self.n, self.d = result.n, result.d
        return self
    
    def __pow__(self, other) -> Frac:
        if isinstance(other, (int, float)):
            other = Frac(other)
        return Frac(float(self) ** float(other))
    
    def __rpow__(self, other) -> Frac:
        return self.__pow__(other)
    
    def __ipow__(self, other) -> Frac:
        result = self ** other
        self.n, self.d = result.n, result.d
        return self

    def __mod__(self, other) -> Frac:
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self.n * other.d % (self.d * other.n)
        new_d = self.d * other.d
        return Frac(new_n / new_d)
    
    def __rmod__(self, other) -> Frac:
        return self.__mod__(other)
    
    def __imod__(self, other) -> Frac:
        result = self % other
        self.n, self.d = result.n, result.d
        return self

    def __neg__(self) -> Frac:
        return Frac(-self.n, self.d)
    
    def __pos__(self) -> Frac:
        return Frac(self.n, self.d)
    
    def __invert__(self) -> Frac:
        return Frac(self.d, self.n)
    
    def __abs__(self) -> Frac:
        return Frac(abs(self.n), abs(self.d))
    
    def __floor__(self) -> Frac:
        return Frac(self.n // self.d)
    
    def __round__(self, n: int = 0) -> float:
        return round(float(self), n)

    #endregion Arithmetic operators
    def __eq__(self, other) -> bool:
        other = self._to_fraction(other)
        if other is not None:
            return self._n * other._d == self._d * other._n
        return False

    def __ne__(self, other) -> bool:
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


def _perform_tests():
    one_third = 0.33333333333

    assert Frac(one_third) == one_third
    assert tuple(Frac(one_third)) == (1, 3)
    assert str(Frac(one_third)) == "1/3"
    assert abs(Frac(one_third) - one_third) < 0.000001


if __name__ == '__main__':
    _perform_tests()
