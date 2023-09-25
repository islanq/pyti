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
            raise ZeroDivisionError("The denominator cannot be 0!")
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
        return (self.n, self.d)

    def __set__(self) -> set:
        return {self.n, self.d}

    def __list__(self) -> list:
        return [self.n, self.d]
    
    def __str__(self) -> str:
        return "{}/{}".format(self.n, self.d) if self.approx != int(self) else str(int(self))

    def __repr__(self):
        return "{}/{}".format(self.n, self.d) if self.approx != int(self) else str(int(self))

    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Frac(other)
        new_n = self._n * other._d + other._n * self._d
        new_d = self._d * other._d
        return Frac(new_n / new_d)

    def __abs__(self):
        return abs(self.n / self.d)

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
