import re
from re import search, match, compile

_digit_pat = r'^(-)?\d+$'
_numeric_pat = r'^(-)?\d+(\.\d+)?$'
_alpha_pat = r'^[a-zA-Z]+$'
_alnum_pat = r'^(-)?[a-zA-Z0-9.]+$'

_digit_re = compile(_digit_pat)
_numeric_re = compile(_numeric_pat)
_alpha_re = compile(_alpha_pat)
_alnum_re = compile(_alnum_pat)

def is_digit(s):
    s = str(s) if not isinstance(s, str) else s
    try:
        return re.match(_digit_re, s) is not None
    except ValueError:
        return match(_digit_re, s) is not None
    finally:
        return match(_digit_pat, s) is not None

def is_numeric(s):
    s = str(s) if not isinstance(s, str) else s
    try:
        return re.match(_numeric_re, s) is not None
    except ValueError:
        return match(_numeric_re, s) is not None
    finally:
        return match(_numeric_pat, s) is not None
    
def is_alpha(s):
    s = str(s) if not isinstance(s, str) else s
    try:
        return re.match(_alpha_re, s) is not None
    except ValueError:
        return match(_alpha_re, s) is not None
    finally:
        return match(_alpha_pat, s) is not None

def is_alnum(s):
    s = str(s) if not isinstance(s, str) else s
    try:
        return re.match(_alnum_re, s) is not None
    except ValueError:
        return match(_alnum_re, s) is not None
    finally:
        return match(_alnum_pat, s) is not None
    
"""
For some reason, the TI CAS system was NOT having the regex,
however, it is much faster than the ord methods, and it is
more accurate in a lot of ways as well. 

That is why there is so much emphasis on the regex, and the
exagerated amount of code to make sure that it is working

    is_digit = lambda s: match(_digit_re, s) is not None
    is_numeric = lambda s: match(_numeric_re, s) is not None
    is_alpha = lambda s: match(_alpha_re, s) is not None
    is_alnum = lambda s: match(_alnum_re, s) is not None
    is_integer = lambda s: is_digit(s) and not is_numeric(s)

    if not 're' in dir():
    is_digit = lambda s: 
    is_numeric = lambda s: match(r'^(−|-)?\d+(.\d+)?$', s) is not None
    is_alpha = lambda s: match(r'^[a-zA-Z]+$', s) is not None
    is_alnum = lambda s: match('^(−|\-)?[a-zA-Z0-9.]+$', s) is not None
    is_integer = lambda s: is_digit(s) and not is_numeric(s)
    def is_digit(s):
    if '-' in s and not s.startswith('-') or s and s.count('-') > 1:
    return False
    return all(48 <= ord(c) <= 57 or ord(c) == 45 for c in s)

    def is_numeric(s):
    if '.' in s and s.count('.') > 1:
    return False
    if '-' in s and not s.startswith('-') or s.count('-') > 1:
    return False
    return all(48 <= ord(c) <= 57 or 45 <= ord(c) <= 46 for c in s)
    
    def is_alpha(s):
    return all(65 <= ord(c) <= 90 or 97 <= ord(c) <= 122 for c in s)
    
    def is_alnum(s):
    return is_alpha(s) or is_digit(s) or is_numeric(s)
 
 """
 
'''
 BISECT (from bisect.py)
'''

def insort_right(a, x, lo=0, hi=None, *, key=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the right of the rightmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    if key is None:
        lo = bisect_right(a, x, lo, hi)
    else:
        lo = bisect_right(a, key(x), lo, hi, key=key)
    a.insert(lo, x)


def bisect_right(a, x, lo=0, hi=None, *, key=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(i, x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    # Note, the comparison uses "<" to match the
    # __lt__() logic in list.sort() and in heapq.
    if key is None:
        while lo < hi:
            mid = (lo + hi) // 2
            if x < a[mid]:
                hi = mid
            else:
                lo = mid + 1
    else:
        while lo < hi:
            mid = (lo + hi) // 2
            if x < key(a[mid]):
                hi = mid
            else:
                lo = mid + 1
    return lo


def insort_left(a, x, lo=0, hi=None, *, key=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.

    If x is already in a, insert it to the left of the leftmost x.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if key is None:
        lo = bisect_left(a, x, lo, hi)
    else:
        lo = bisect_left(a, key(x), lo, hi, key=key)
    a.insert(lo, x)

def bisect_left(a, x, lo=0, hi=None, *, key=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(i, x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    # Note, the comparison uses "<" to match the
    # __lt__() logic in list.sort() and in heapq.
    if key is None:
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid
    else:
        while lo < hi:
            mid = (lo + hi) // 2
            if key(a[mid]) < x:
                lo = mid + 1
            else:
                hi = mid
    return lo


# Overwrite above definitions with a fast C implementation
try:
    from _bisect import *
except ImportError:
    pass

# Create aliases
bisect = bisect_right
insort = insort_right