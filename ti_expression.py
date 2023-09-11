
import sys

if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../'])
    
from wrappers import extends_method_names
from parsing import parse_expression, parse_variables
from polyfill import is_digit, is_alnum, is_alpha, is_numeric
from ti_interop import tiexec, is_ti_type


@extends_method_names
class TiExpression:

    def __init__(self, expr=None):
        self.expr_str = expr if isinstance(expr, str) else str(expr)
        if self.expr_str != "":
            self.expr = parse_expression(self.expr_str)
            self.vars = parse_variables(self.expr_str)
        else:
            self.expr = None
            self.vars = None

    def __str__(self):
        return self.expr_str

    def __repr__(self) -> str:
        return self.expr_str

    @property
    def numeric(self):
        return is_numeric(self.expr_str)

    def symbolic(self):
        return is_alnum(self.expr_str)

    def right(self):
        return tiexec('right("{}")'.format(self.expr_str))

    def left(self):
        return tiexec('left("{}")'.format(self.expr_str))

    def concat(self, other):
        self.expr_str += str(other)

    def __TiMatrix__(self):
        from ti_collections import TiCollections
        if TiCollections.is_ti_mat(self.expr_str):
            return TiCollections.to_ti_mat(self.expr_str)

    def __add__(self, other):
        if not isinstance(other, str):
            other = str(other)
        return TiExpression(tiexec("({})+({})".format(str(self), other)))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, str):
            other = str(other)
        return TiExpression(tiexec("({})-({})".format(str(self), other)))

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if not isinstance(other, str):
            other = str(other)
        return TiExpression(tiexec("({})*({})".format(str(self), other)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, str):
            other = str(other)
        return TiExpression(tiexec("({})/({})".format(str(self), other)))

    def __rtruedive__(self, other):
        return self.__truediv__(other)

    def __pow__(self, other):
        if not isinstance(other, str):
            other = str(other)
        return TiExpression(tiexec("({})^({})".format(self.expr_str, other.expr_str)))

    def __rpow__(self, other):
        return self.__pow__(other)

    def var_count(self):
        return len(self.vars)

    def unique_vars(self):
        return list(set(self.vars))

    def _get_expr_per_type(self, expr_str):
        if expr_str is None:
            return None

        if isinstance(expr_str, str):
            return TiExpression(expr_str)
        elif isinstance(expr_str, TiExpression):
            return expr_str.expr_str
        else:
            raise TypeError("expr_str must be a string or TiExpression")
