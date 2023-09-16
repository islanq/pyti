from collections import namedtuple

# Define the mappings for superscript and subscript characters
superscript_mapping = {
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹',
    '+': '⁺',
    '-': '⁻',
    '=': '⁼',
    '(': '⁽',
    ')': '⁾',
    'a': 'ᵃ',
    'b': 'ᵇ',
    'c': 'ᶜ',
    'd': 'ᵈ',
    # Add more mappings as needed
}

subscript_mapping = {
    '0': '₀',
    '1': '₁',
    '2': '₂',
    '3': '₃',
    '4': '₄',
    '5': '₅',
    '6': '₆',
    '7': '₇',
    '8': '₈',
    '9': '₉',
    '+': '₊',
    '-': '₋',
    '=': '₌',
    '(': '₍',
    ')': '₎',
    'a': 'ₐ',
    'e': 'ₑ',
    'h': 'ₕ',
    'i': 'ᵢ',
    # Add more mappings as needed
}

# Define the named tuple for character, superscript, and subscript
CharScripts = namedtuple('CharScripts', ['char', 'super', 'sub'])


def char_to_superscript(char):
    if not isinstance(char, str):
        char = str(char)
    return superscript_mapping.get(char, char)


def char_to_subscript(char):
    if not isinstance(char, str):
        char = str(char)
    return subscript_mapping.get(char, char)


def has_superscript(char):
    return char in superscript_mapping


def has_subscript(char):
    return char in subscript_mapping


def char_superscript(char):
    if not isinstance(char, str):
        char = str(char)
    if char in superscript_mapping:
        return superscript_mapping[char]
    elif char.isnumeric():
        return ''.join([chr(ord(digit) + 8272) for digit in char])
    else:
        return char


def char_subscript(char):
    if not isinstance(char, str):
        char = str(char)
    if char in subscript_mapping:
        return subscript_mapping[char]
    elif char.isnumeric():
        return ''.join([chr(ord(digit) + 8320) for digit in char])
    else:
        return char
