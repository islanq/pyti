from cachable import Cachable as _Cachable
from collections import namedtuple as _namedtuple
import sys
import re as _re
from adt import AbstractDataType

sys.path.extend(['../lib/', './lib/', '../', '.'])
_Span = _namedtuple('Span', ['start', 'end'])


class Match:
    def __init__(self, match_string: str, native_match, start: int, end: int):
        self.match_str = match_string
        self.native_match = native_match
        self._start = start
        self._end = end
        # self._groups = native_match.groups if native_match else None
        self._groups = (match_string,) + \
            (native_match.groups() if native_match else ())

    @property
    def start(self) -> int:
        """Returns the start index of the match."""
        return self._start

    @property
    def end(self) -> int:
        """Returns the end index of the match."""
        return self._end

    @property
    def match(self):
        """Returns the matched string."""
        return self.native_match

    @property
    def string(self):
        return self.match_str

    def groups(self):
        return self.native_match.groups()

    def group(self, index: int = 0) -> str:
        """Returns the matched string or a specified group."""
        try:
            return self._groups[index]
        except IndexError:
            raise IndexError('No such group')

    def span(self) -> _Span:
        """Returns a tuple containing the start and end indices of the match."""
        return _Span(self.start, self.end)

    def __str__(self) -> str:
        try:
            match_str = self.group(0)
        except IndexError:
            match_str = ""
        return "<Regex.Match object; span=({}, {}); match='{}'>".format(self.span().start, self.span().end, match_str)

    def __repr__(self) -> str:
        return self.__str__()


class RegexFlags(AbstractDataType):

    NONE = AbstractDataType(0, 'NONE')
    ASCII = AbstractDataType(256, 'ASCII')
    DEBUG = AbstractDataType(128, 'DEBUG')
    IGNORECASE = I = AbstractDataType(2, 'IGNORECASE')
    LOCALE = L = AbstractDataType(4, 'LOCALE')
    UNICODE = U = AbstractDataType(32, 'UNICODE')
    MULTILINE = M = AbstractDataType(8, 'MULTILINE')
    DOTALL = S = AbstractDataType(16, 'DOTALL')
    VERBOSE = X = AbstractDataType(64, 'VERBOSE')
    TEMPLATE = T = AbstractDataType(1, 'TEMPLATE')


class Regex:

    @staticmethod
    def compile(pattern: str, flags: RegexFlags = RegexFlags.NONE):
        return Pattern(pattern, flags)

    @staticmethod
    def match(pattern: str, string: str, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None):
        return Pattern(pattern, flags).match(string, start, end)

    @staticmethod
    def search(pattern: str, string: str, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None):
        return Pattern(pattern, flags).search(string, start, end)

    @staticmethod
    def sub(pattern: str, repl: str, string: str, count=0, flags: RegexFlags = RegexFlags.NONE):
        return Pattern(pattern, flags).sub(repl, string, count)

    @staticmethod
    def subn(pattern: str, repl: str, string: str, count: int = 0, flags: RegexFlags = RegexFlags.NONE):
        return Pattern(pattern, flags).subn(repl, string, count)

    @staticmethod
    def findall(pattern: str, string: str, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None):
        return Pattern(pattern, flags).findall(string, start, end)

    @staticmethod
    def split(pattern: str, string: str, maxsplit: int = 0, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None):
        return Pattern(pattern, flags).split(string, maxsplit, start, end)

    @staticmethod
    def finditer(pattern: str, string: str, start: int = 0, end: int = None):
        return Pattern(pattern).finditer(string, start, end)

    @staticmethod
    def fullmatch(pattern: str, string: str, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None):
        return Pattern(pattern, flags).fullmatch(string, start, end)


class Pattern(_Cachable):

    def __init__(self, pattern, flags: RegexFlags = RegexFlags.NONE, force_custom_impl=False) -> None:

        self._has_re_span = sys.implementation.name != 'micropython'
        self._forced = force_custom_impl
        self._pattern_string = pattern
        self._pattern_flags = flags
        self._pattern_renew = True

        self._search_method = None
        self._match_method = None

        self._update_pattern()
        self._initialized = True

        if self._forced and self._has_re_span:
            self._has_re_span = False
            print("Forcing custom re.match implementation")
            print("This message will only display if")
            print("the default re.match implementation is available")
            print("and the custom implementation is being used")
            print("Confirming has_re_span is {}:".format(self._has_re_span))

    @property
    def flags(self):
        return self._pattern_flags

    @property
    def pattern(self):
        return self._pattern


# region methods

    def match(self, string: str, start: int = 0, end: int = None, omit_positions: bool = False):
        """Implements the match method using re.match."""
        return self._find(self._match_method, string, start, end, omit_positions)

    def search(self, string: str, start: int = 0, end: int = None, omit_positions: bool = False):
        """Implements the search method using re.search."""
        return self._find(self._search_method, string, start, end, omit_positions)

    def _find(self, method: callable, string: str, start: int = 0, end: int = None, omit_positions: bool = False):
        """Helper method to implement common logic for match and search."""
        if end is None:
            end = len(string)

        m = method(string[start:end])
        if not m:
            return None

        if omit_positions:
            return Match(m.group(0), None, None)

        return self._process_match(m.group(0), m, string, start, end)

    def findall(self, string: str, start: int = 0, end: int = None):
        """ Implements the findall method using custom implementation."""
        return [m.string for m in self.finditer(string, start, end)]

    def split(self, string: str, maxsplit: int = 0):
        """Implements the split method using re.split."""
        # Find all the match objects in the string
        matches = list(self.finditer(string))

        # If no matches, return the string in a list
        if not matches:
            return [string]

        # Split the string at the match indices
        splits = []
        start = 0
        for i, match in enumerate(matches):
            if maxsplit and i >= maxsplit:
                break

            splits.append(string[start:match.start])
            start = match.end

        # Append the remaining part of the string
        splits.append(string[start:])
        return [s for s in splits if s != '']

    def split_leg(self, string: str, maxsplit: int = 0, start: int = 0, end: int = None):
        """Implements the split method using custom implementation."""
        if end is None:
            end = len(string)

        parts = []
        pos = start
        split_count = 0
        while pos < end and (not maxsplit or split_count < maxsplit):
            match = self.search(string, pos, end)
            if not match:
                break
            parts.append(string[pos:match.start])
            pos = match.end
            split_count += 1
        parts.append(string[pos:end])
        return parts

    def finditer(self, string, start=0, end=None):
        """Implements the finditer method using custom implementation."""
        if end is None:
            end = len(string)

        pos = start
        while pos < end:
            native_match = self.search(string, pos, end)
            if not native_match:
                break

            # Use the correct arguments while creating a new Match instance
            yield Match(native_match.match_str, native_match, native_match._start, native_match._end)

            pos = native_match._end if native_match._end > pos else pos + 1

    def fullmatch(self, string: str, start: int = 0, end: int = None):
        """Implements the fullmatch method using custom implementation."""
        if end is None:
            end = len(string)

        match = self.match(string, start, end)
        if match and match.start == start and match.end == end:
            return match

        return None

    def sub(self, repl, string, count=0):
        """Implements the sub method using custom implementation."""
        result = ''
        pos = 0
        for i, match in enumerate(self.finditer(string)):
            if count and i >= count:
                break
            result += string[pos:match.start] + repl
            pos = match.end
        result += string[pos:]
        return result

    def subn(self, repl: str, string: str, count: int = 0):
        """Implements the subn method using custom implementation."""
        result = ''
        pos = 0
        substitutions = 0

        for i, match in enumerate(self.finditer(string)):
            if count and i >= count:
                break
            result += string[pos:match.start] + repl
            pos = match.end
            substitutions += 1

        result += string[pos:]
        return result, substitutions

    def _find_match_positions(self, string, start, end):
        """Find the start and end positions of a match using a binary search approach."""

        if self._search_method(string[start:end]):
            # if a match is confirmed, proceed with binary search
            left, right = start, end

            # Step 2 & 3: Binary search to narrow down to a small segment
            while right - left > 10:  # Adjust threshold as needed
                mid = left + (right - left) // 2
                if self._search_method(string[left:mid]):
                    right = mid
                else:
                    left = mid

            # Step 4: Linear search in the small segment to find exact positions
            for start_pos in range(left, right):
                match = self._match_method(string[start_pos:])
                if match:
                    end_pos = start_pos + len(match.group(0))
                    return start_pos, end_pos
        else:
            return None, None

    def _process_match(self, match_str: str, native_match, string, start, end):
        if self._has_re_span:
            # This will work in full Python environments
            span = native_match.span()
            start_pos = start + span[0]
            end_pos = start + span[1]
        else:
            # If there is no "span" attribute, it means we are in a reduced Python environment
            # Use the custom method to find the start and end positions
            start_pos, end_pos = self._find_match_positions(string, start, end)
        return Match(match_str, native_match, start_pos, end_pos)

    def _update_pattern(self):

        pattern = self._pattern_string
        flags = self._pattern_flags

        try:
            self._pattern = _re.compile(pattern, flags)
            self._search_method = self._pattern.search
            self._match_method = self._pattern.match
        except _re.error:
            self._pattern = pattern
            self._search_method = _re.search
            self._match_method = _re.match

        self._pattern_renew = False

# endregion methods


if __name__ == '__main__':

    match_pattern = r'(ab|123)'
    pat = Pattern(match_pattern, force_custom_impl=True)
    assert pat._has_re_span == False and pat._forced == True
    assert pat.search('abc123deab123fab').groups() == _re.search(match_pattern, 'abc123deab123fab').groups()
    assert pat.findall('abc123deab123fab') == _re.findall(match_pattern, 'abc123deab123fab')
    assert pat.search('abc123def').span() == _re.search(match_pattern, 'abc123def').span()
    assert pat.split('abc123def') == ['c', 'def']
    assert pat.sub('X', 'abc123def') == 'XcXdef'
    assert pat.subn('X', 'abc123def') == ('XcXdef', 2)
    print('all basic assertions passed')
