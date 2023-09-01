'''
    is_digit = lambda s: all(48 <= ord(c) <= 57 for c in s)
    is_numeric = lambda s: all(48 <= ord(c) <= 57 or ord(c) == 46 for c in s)
    is_alpha = lambda s: all(65 <= ord(c) <= 90 or 97 <= ord(c) <= 122 for c in s)
    is_alnum = lambda s: is_alpha(s) or is_digit(s) or is_numeric(s)
'''
import re
# Compiled regex
_digit_re = re.compile(r'^\d+$')
_numeric_re = re.compile(r'^\d+(\.\d+)?$')
_alpha_re = re.compile(r'^[a-zA-Z]+$')
_alnum_re = re.compile(r'^[a-zA-Z0-9.]+$')

is_digit = lambda s: re.match(_digit_re, s) != None
is_numeric = lambda s: re.match(_numeric_re, s) != None
is_alpha = lambda s: re.match(_alpha_re, s) != None
is_alnum = lambda s: re.match(_alnum_re, s) != None
is_integer = lambda s: is_digit(s) and not is_numeric(s)