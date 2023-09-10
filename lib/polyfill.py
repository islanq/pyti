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

def reduce_quotes(text):
    """Removes all empty quote pairs from a string."""
    # Step 1: Find the middle index to split the string in half
    middle_idx = len(text) // 2
    lhs = text[:middle_idx]
    rhs = text[middle_idx:]
    
    # Step 2: Count the quotes in each half
    lhs_count = lhs.count("'") + lhs.count('"')
    rhs_count = rhs.count("'") + rhs.count('"')
    
    # Step 3: Ensure even number of quotes in each half
    if lhs_count % 2 != 0:
        # Find and remove the first quote from the left half
        for q in ['"', "'"]:
            if q in lhs:
                lhs = lhs.replace(q, "", 1)
                break
                
    if rhs_count % 2 != 0:
        # Find and remove the first quote from the right half
        for q in ['"', "'"]:
            if q in rhs:
                rhs = rhs.replace(q, "", 1)
                break
                
    # Step 4: Join the two halves back together
    balanced_text = lhs + rhs
    
    # Step 5: Continuously remove empty quote pairs until none are left
    while any(q in balanced_text for q in ['""', "''"]):
        balanced_text = balanced_text.replace('""', '').replace("''", '')

    return balanced_text