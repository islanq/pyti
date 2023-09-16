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


def create_varied_sequence(head: str, tail: str, sequence: str = ' ', max: int = 100) -> list:
    """_summary_

    Args:
        head (str): _description_ start
        tail (str): _description_ end
        sequence (str, optional): _description_. Defaults to ' '.
        max (int, optional): _description_. Defaults to 100.

    Returns:
        list: _description_
    """
    return [head + sequence * i + tail for i in range(max)]


def get_max_sequence(string: str, sequence: str=' ') -> int:
    """_summary_

    Args:
        string (str): _description_ string to search within
        sequence (str, optional): _description_. the repitition str Defaults to ' '.

    Returns:
        int: _description_ max number of times sequence is repeated in string
    """
    str_len = len(string)
    seq_len = len(sequence)
    # sequence is not a substring of string
    if seq_len > str_len:
        return 0
    # sequence is empty
    if sequence not in string:
        return 0
    if sequence == '':
        return str_len
    if sequence == string:
        return 1
    
    
def get_max_between(string: str, head: str, tail: str, pattern: str = ' ') -> int:
    """_summary_

    Args:
        string (str): _description_ string to search within
        head (str): _description_ start of substring
        tail (str): _description_ end of substring
        pattern (str, optional): _description_. pattern Defaults to ' '.

    Returns:
        int: _description_
    """
    head_len = len(head)
    tail_len = len(tail)
    
    # Get all indices of head and tail substrings in the input string
    head_indices = [i for i in range(len(string)) if string.startswith(head, i)]
    tail_indices = [i for i in range(len(string)) if string.startswith(tail, i)]
    
    max_len = 0
    
    # Iterate over all head and tail pairs to find the longest substring between them
    for head_index in head_indices:
        for tail_index in tail_indices:
            if head_index + head_len < tail_index:
                substring_between = string[head_index + head_len : tail_index]
                
                # If a pattern is specified, check if it is contained in the substring
                if pattern and pattern not in substring_between:
                    continue
                
                # Update max_len if the current substring is longer than the previously found substrings
                max_len = max(max_len, len(substring_between))
    
    return max_len


def map_replace(string, **replacement_map):
    """_summary_

    Args:
        string (_type_): _description_
        replacement_map (_type_): _description_

    Returns:
        _type_: _description_
    """
    for old, new in replacement_map.items():
        string = string.replace(old, new)
    return string