import math


class AbstractArithmeticException(Exception):
    def __init__(self, message: str = 'An arithmetic errow occurred') -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class AbstractAddException(AbstractArithmeticException):
    def __init__(self, message: str = 'Cannot add these types') -> None:
        super().__init__(message)


class AbstractMulException(AbstractArithmeticException):
    def __init__(self, message: str = 'Cannot multiply these types') -> None:
        super().__init__(message)


class AbstractSubException(AbstractArithmeticException):
    pass


class AbstractDivException(AbstractArithmeticException):
    pass


class AbstractDataType:

    def __init__(self, value, name, *compatible_types) -> None:
        self._value = value
        self._name = name
        self._type = type(value)
        self._compatible_types = (self._type,) + compatible_types

    @property
    def value(self) -> any:
        return self._value

    @property
    def name(self) -> str:
        return self._name

    @property
    def combatible(self) -> tuple[type]:
        return self._compatible_types

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, self.combatible):
            return self.value == __value
        if isinstance(__value, AbstractDataType):
            return self.value == __value.value
        return False

    def __str__(self) -> str:
        try:
            return str(self.value)
        except:
            return self._name

    def __add__(self, other):
        if isinstance(other, self.combatible):
            return self._type(self.value + other)
        raise AbstractAddException(
            'Cannot add {} to {}'.format(type(other), type(self)))

    def __iadd__(self, other):
        if isinstance(other, self._type):
            self._value += other
            return self

        if isinstance(other, AbstractDataType):
            try:
                self._value += other.value
                return self
            except:
                self._value += other
                return self

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value - other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value - other.value)
            except:
                return self._type(self.value - other)

    def __isub__(self, other):
        if isinstance(other, self._type):
            self._value -= other
            return self

        if isinstance(other, AbstractDataType):
            try:
                self._value -= other.value
                return self
            except:
                self._value -= other
                return self

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value * other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value * other.value)
            except:
                return self._type(self.value * other)

    def __imul__(self, other):
        if isinstance(other, self._type):
            self._value *= other
            return self

        if isinstance(other, AbstractDataType):
            try:
                self._value *= other.value
                return self
            except:
                self._value *= other
                return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value / other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value / other.value)
            except:
                return self._type(self.value / other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __itruediv__(self, other):
        if isinstance(other, self._type):
            self._value /= other
            return self

        if isinstance(other, AbstractDataType):
            try:
                self._value /= other.value
                return self
            except:
                self._value /= other
                return self

    def __floordiv__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value // other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value // other.value)
            except:
                return self._type(self.value // other)

    def __rfloordiv__(self, other):
        return self.__floordiv__(other)

    def __mod__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value % other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value % other.value)
            except:
                return self._type(self.value % other)

    def __rmod__(self, other):
        return self.__mod__(other)

    def __pow__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value ** other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value ** other.value)
            except:
                return self._type(self.value ** other)

    def __rpow__(self, other):
        return self.__pow__(other)

    def __lshift__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value << other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value << other.value)
            except:
                return self._type(self.value << other)

    def __rlshift__(self, other):
        return self.__lshift__(other)

    def __rshift__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value >> other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value >> other.value)
            except:
                return self._type(self.value >> other)

    def __rrshift__(self, other):
        return self.__rshift__(other)

    def __and__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value & other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value & other.value)
            except:
                return self._type(self.value & other)

    def __rand__(self, other):
        return self.__and__(other)

    def __xor__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value ^ other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value ^ other.value)
            except:
                return self._type(self.value ^ other)

    def __rxor__(self, other):
        return self.__xor__(other)

    def __or__(self, other):
        if isinstance(other, self._type):
            return self._type(self.value | other)

        if isinstance(other, AbstractDataType):
            try:
                return self._type(self.value | other.value)
            except:
                return self._type(self.value | other)

    def __ror__(self, other):
        return self.__or__(other)

    def __neg__(self):
        return self._type(-self.value)

    def __pos__(self):
        return self._type(+self.value)

    def __abs__(self):
        return self._type(abs(self.value))

    def __invert__(self):
        return self._type(~self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __complex__(self):
        return complex(self.value)

    def __round__(self, n=None):
        return round(self.value, n)

    def __floor__(self):
        return math.floor(self.value)

    def __ceil__(self):
        return math.ceil(self.value)

    def __trunc__(self):
        return math.trunc(self.value)

    def __index__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def values(cls) -> list[any]:
        return [abv.value for _, abv in cls.__dict__.items() if isinstance(abv, AbstractDataType)]

    @classmethod
    def names(cls) -> list[str]:
        return [abv.name for _, abv in cls.__dict__.items() if isinstance(abv, AbstractDataType)]

    @classmethod
    def items(cls) -> dict[str, any]:
        return {abv.name: abv.value for _, abv in cls.__dict__.items() if isinstance(abv, AbstractDataType)}
