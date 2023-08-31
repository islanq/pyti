is_digit = lambda s: all(48 <= ord(c) <= 57 for c in s)
is_numeric = lambda s: all(48 <= ord(c) <= 57 or ord(c) == 46 for c in s)
is_alpha = lambda s: all(65 <= ord(c) <= 90 or 97 <= ord(c) <= 122 for c in s)
is_alnum = lambda s: is_alpha(s) or is_digit(s) or is_numeric(s)