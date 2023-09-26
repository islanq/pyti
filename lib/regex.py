from cachable import Cachable as _Cachable
from collections import namedtuple as _namedtuple
import sys
import re as _re
from adt import AbstractDataType

sys.path.extend(['../lib/', './lib/', '../', '.'])
_Span = _namedtuple('Span', ['start', 'end'])


class Span:

    def __init__(self, start=0, end=None) -> None:

        if isinstance(start, tuple):
            self._start = start[0]
            self._end = start[1]
        elif isinstance(start, Span):
            self._start = start._start
            self._end = start._end
        elif isinstance(start, int) and isinstance(end, int):
            self._start = start
            self._end = end
        elif isinstance(start, set):
            self._start = start.pop()
            self._end = start.pop()
        elif isinstance(start, list):
            self._start = start[0]
            self._end = start[1]
        elif isinstance(start, dict):
            if 'start' in start and 'end' in start:
                self._start = start['start']
                self._end = start['end']
            else:
                keys = start.keys()
                self._start = start[keys[0]]
                self._end = start[keys[1]]
        elif isinstance(start, str):
            self._start = int(start.split(',')[0].strip().replace('(', ''))
            self._end = int(start.split(',')[1].strip().replace(')', ''))
        elif isinstance(start, float) and end:
            self._start = int(start)
            self._end = int(end)
        else:
            raise TypeError('Invalid argument types')

# region Properties
    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    @start.setter
    def start(self, value: int) -> None:
        self._start = value

    @end.setter
    def end(self, value: int) -> None:
        self._end = value
# endregion Properties

# region Dunder Methods

# region Conversion Methods

    def __str__(self) -> str:
        return 'Span({}, {})'.format(self._start, self._end)

    def __int__(self) -> int:
        return self._end - self._start

    def __float__(self) -> float:
        return self._end - self._start

    def __len__(self) -> int:
        return abs(self._end - self._start)

    def __tuple__(self) -> _Span:
        return _Span(self._start, self._end)

    def __set__(self) -> set:
        return {self._start, self._end}

    def __dict__(self) -> dict:
        return {'start': self._start, 'end': self._end}

    def __list__(self) -> list:
        return [self._start, self._end]

# endregion Conversion Methods

# region Behaviors Methods

    def __getitem__(self, index: int) -> int:
        return (self._start, self._end)[index]

    def __setitem__(self, index: int, value: int) -> None:
        if index == 0:
            self._start = value
        elif index == 1:
            self._end = value
        else:
            raise IndexError('Index out of range')

    def __iter__(self):
        return iter((self._start, self._end))

    def __hash__(self) -> int:
        return hash((self._start, self._end))

    def __bool__(self) -> bool:
        return self._start != 0 or self._end != 0

# endregion Behaviors Methods

# region Comparison Operators

    def __eq__(self, o: object) -> bool:
        if isinstance(o, tuple):
            return self.__eq_tuple__(o)
        elif isinstance(o, Span):
            return self.__eq_span__(o)
        else:
            raise TypeError('Invalid argument type')

    def __eq_tuple__(self, o: tuple) -> bool:
        return self._start == o[0] and self._end == o[1]

    def __eq_span__(self, o: _Span) -> bool:
        return self._start == o.start and self._end == o.end

    def __ne__(self, o: object) -> bool:
        return self._start != o.start or self._end != o.end

    def __lt__(self, o: object) -> bool:
        return self._start < o.start and self._end < o.end

    def __le__(self, o: object) -> bool:
        return self._start <= o.start and self._end <= o.end

    def __gt__(self, o: object) -> bool:
        return self._start > o.start and self._end > o.end

    def __ge__(self, o: object) -> bool:
        return self._start >= o.start and self._end >= o.end

# endregion Comparison Operators

# region Arithmetic Operators

    def __add__(self, o: object):
        if isinstance(o, Span):
            return self.__add_span__(o)
        elif isinstance(o, tuple):
            return self.__add_tuple__(o)
        elif isinstance(o, _Span):
            return self.__add_Span__(o)
        elif isinstance(o, int):
            return self.__add_int__(o)
        elif isinstance(o, float):
            return self.__add_float__(o)
        else:
            raise TypeError('Invalid argument type')

    def __add_span__(self, o: 'Span'):
        return Span(self._start + o._start, self._end + o._end)

    def __add_tuple__(self, o: tuple):
        return Span(self._start + o[0], self._end + o[1])

    def __add_Span__(self, o: _Span):
        return Span(self._start + o.start, self._end + o.end)

    def __add_int__(self, o: int):
        return Span(self._start + o, self._end + o)

    def __add_float__(self, o: float):
        return Span(int(self._start + o), (self._end + o))

    def __radd__(self, o: object):
        return self.__add__(self, o)

    def __iadd__(self, o: object):
        return self.__add__(self, o)

    def __sub__(self, o: object):
        return Span(self._start - o.start, self._end - o.end)

    def __rsub__(self, o: object):
        return Span(self._start - o.start, self._end - o.end)

    def __isub__(self, o: object):
        return Span(self._start - o.start, self._end - o.end)

    def __mul__(self, o: object):
        if isinstance(o, Span):
            return self.__mul_span__(o)
        elif isinstance(o, int):
            return self.__mul_int__(o)
        elif isinstance(o, float):
            return self.__mul_float__(o)
        else:
            raise TypeError('Invalid argument type')

    def __mul_span__(self, o: 'Span'):
        return Span(self._start * o._start, self._end * o._end)

    def __mul_int__(self, o: int):
        return Span(self._start * o, self._end * o)

    def __mul_float__(self, o: float):
        return Span(self._start * o, self._end * o)

    def __rmul__(self, o: object):
        return self.__mul__(self, o)

    def __imul__(self, o: object):
        if isinstance(o, Span):
            return self.__imul_span__(o)
        elif isinstance(o, int):
            return self.__imul_int__(o)
        elif isinstance(o, float):
            return self.__imul_float__(o)
        else:
            raise TypeError('Invalid argument type')

    def __imul_int__(self, o: int):
        return Span(self._start * o, self._end * o)

    def __imul_float__(self, o: float):
        return Span(self._start * o, self._end * o)

    def __imul_span__(self, o: 'Span'):
        return Span(self._start * o._start, self._end * o._end)

    def __truediv__(self, o: object):
        return Span(self._start / o.start, self._end / o.end)

    def __rtruediv__(self, o: object):
        return Span(self._start / o.start, self._end / o.end)

    def __itruediv__(self, o):
        return Span(self._start / o.start, self._end / o.end)

# endregion Arithmetic Operators

    def __repr__(self) -> str:
        return 'Span({}, {})'.format(self._start, self._end)

# endregion Dunder Methods

    def offset(self, offset: (int, 'Span'), start: bool = True, end: bool = True):
        if isinstance(offset, Span):
            beg = offset._start if start else 0
            end = offset._end if end else 0
        else:
            beg = offset if start else 0
            end = offset if end else 0
        return Span(self._start + beg, self._end + end)

    def swap(self) -> 'Span':
        return Span(self._end, self._start)


class Match:
    def __init__(self, match, start: int, end: int):
        self._span = (Span(start, end),)
        self._groups = ()
        self._group = ()

        """ 
        we'll assume the most matches we can have 
        is the length of the match string, as this would
        mean every character matches at least once
        """
        # generate the span objects for each match group
        mstring = match.group(0)
        for i in range(1, len(match.group(0))):
            try:
                group = match.group(i)
                group_len = len(group)
                if i == 1:
                    beg = 0
                    end = group_len
                else:
                    mst = mstring[self.span(i-1)._end:]
                    beg = self.span(i-1)._end + mst.find(group)
                    end = beg + group_len
                self._span = self._span + (Span(beg, end),)
            except:
                break
        """
        build out the groups based on the group as that is the
        only object that is guaranteed to be present accross all
        implementations
        """
        for i in range(len(self._span)):
            if i == 0:
                self._group = self._group + (match.group(i),)
            else:
                self._group = self._group + (match.group(i),)
                self._groups = self._groups + (match.group(i),)

    def start(self) -> int:
        """Returns the start index of the match."""
        return self.span().start

    def end(self) -> int:
        """Returns the end index of the match."""
        return self.span().end

    def groups(self) -> tuple[int, int]:
        return self._groups

    def group(self, index: int = 0) -> str:
        try:
            return self._group[index]
        except IndexError:
            raise IndexError('No such group')

    def span(self, index: int = 0, span: Span = None) -> Span:
        """Returns a tuple containing the start and end indices of the match."""
        if span is not None:
            self._insert_span(index, span)
        elif self._span is None:
            return Span(self.start(), self.end())
        return self._span[index]

    def _insert_span(self, index: int, span: Span) -> None:
        spans = self._span
        self._span = ()
        for i in range(len(spans)):
            temp = spans[i] if i != index else span
            self._span = self._span + (temp,)

    def _find_span(self, span: Span) -> int:
        for i in range(len(self._span)):
            if self._span[i] == span:
                return i
        return -1

    def __str__(self) -> str:
        return "<Regex.Match object; span=({}, {}), match='{}'>".format(self.span(0)._start, self.span(0)._end, self.group(0))

    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return len(self._span)


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
    def compile(pattern: str, flags: RegexFlags = RegexFlags.NONE, force=False):
        return Pattern(pattern, flags, force)

    @staticmethod
    def match(pattern: str, string: str, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None, force=False):
        return Pattern(pattern, flags, force).match(string, start, end)
    
    @staticmethod
    def count(pattern: str, string: str, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None, force=False):
        return Pattern(pattern, flags, force).count(string, start, end)

    @staticmethod
    def search(pattern: str, string: str, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None, force=False):
        return Pattern(pattern, flags, force).search(string, start, end)

    @staticmethod
    def sub(pattern: str, repl: str, string: str, count=0, flags: RegexFlags = RegexFlags.NONE, force=False):
        return Pattern(pattern, flags, force).sub(repl, string, count)

    @staticmethod
    def subn(pattern: str, repl: str, string: str, count: int = 0, flags: RegexFlags = RegexFlags.NONE, force=False):
        return Pattern(pattern, flags, force).subn(repl, string, count)

    @staticmethod
    def findall(pattern: str, string: str, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None, force=False):
        return Pattern(pattern, flags, force).findall(string, start, end)

    @staticmethod
    def split(pattern: str, string: str, maxsplit: int = 0, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None, force=False):
        return Pattern(pattern, flags, force).split(string, maxsplit, start, end)

    @staticmethod
    def finditer(pattern: str, string: str, start: int = 0, end: int = None, force=False, flags: RegexFlags = RegexFlags.NONE):
        return Pattern(pattern, flags, force).finditer(string, start, end)

    @staticmethod
    def fullmatch(pattern: str, string: str, flags: RegexFlags = RegexFlags.NONE, start: int = 0, end: int = None, force=False):
        return Pattern(pattern, flags, force).fullmatch(string, start, end)


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

        if self._forced and self._has_re_span:
            self._has_re_span = False
            # print("Forcing custom re.match implementation")

    @property
    def flags(self):
        return self._pattern_flags

    @property
    def pattern(self):
        return self._pattern

    def match(self, string: str, start: int = 0, end: int = None, omit_positions: bool = False) -> Match | None:
        """Implements the match method using re.match."""
        return self._find(self._match_method, string, start, end, omit_positions)

    def count(self, string: str, start: int = 0, end: int = None) -> int:
        """Implements the count method using custom implementation."""
        return len(self.findall(string, start, end))

    def search(self, string: str, start: int = 0, end: int = None, omit_positions: bool = False) -> Match | None:
        return self._find(self._search_method, string, start, end, omit_positions)

    def _find(self, method: callable, string: str, start: int = 0, end: int = None, omit_positions: bool = False) -> Match:
        if end is None:
            end = len(string)

        match = method(string[start:end])
        if not match:
            return None

        # match_str = self._extract_match_str(m, search_str, start, end)

        if omit_positions:
            return Match(match.group(0), None, None)

        return self._process_match(match, string, start, end)

    def findall(self, string: str, start: int = 0, end: int = None) -> list[str]:
        return [m.group(0) for m in self.finditer(string, start, end)]

    def split(self, string: str, maxsplit: int = 0, start: int = 0, end: int = 0) -> list[str]:
        matches = list(self.finditer(string, start, end))

        # If no matches, return the string in a list
        if not matches:
            return [string]

        # Split the string at the match indices
        splits = []
        start = 0
        for i, match in enumerate(matches):
            if maxsplit and i >= maxsplit:
                break

            splits.append(string[start:match.start()])
            start = match.end()

        # Append the remaining part of the string
        splits.append(string[start:])
        return [s for s in splits if s != '']

    def finditer(self, string: str, start: int = 0, end=None):
        """Implements the finditer method using custom implementation."""
        if end is None:
            end = len(string)

        pos = start
        idx = 0
        # while we have matches
        while True:

            match = self.search(string, pos, end)

            if not match:
                break
            # calculate the start and end positions
            s = match.span(0).start+pos
            e = match.span(0).end+pos
            if idx != 0:
                e - len(match.group(0))

            idx += 1
            pos += match.end()

            match.span(0, Span(s, e))

            yield match

    def _process_match(self, match, string: str, start: int, end: int):
        if self._has_re_span:
            # This will work in full Python environments

            span = match.span()
            beg = start + span[0]
            end = start + span[1]

        else:
            # In MicroPython environment, find start and end positions using a custom method
            # start_pos, end_pos = self._find_match_positions(string, start, end)

            beg = string[start:end].index(match.group(0))
            end = beg + len(match.group(0))

           # beg, end = self._find_match_positions(search_str, start, end)

        return Match(match, beg, end)

    def fullmatch(self, string: str, start: int = 0, end: int = None) -> Match | None:
        """Implements the fullmatch method using custom implementation."""
        if end is None:
            end = len(string)

        match = self.match(string, start, end)
        if match and match.start() == start and match.end() == end:
            return match

        return None

    def sub(self, repl: str, string: str, count: int = 0) -> str:
        """Implements the sub method using custom implementation."""
        result = ''
        pos = 0
        for i, match in enumerate(self.finditer(string)):
            if count and i >= count:
                break
            result += string[pos:match.start()] + repl
            pos = match.end()
        result += string[pos:]
        return result

    def subn(self, repl: str, string: str, count: int = 0) -> tuple[str, int]:
        """Implements the subn method using custom implementation."""
        result = ''
        pos = 0
        substitutions = 0

        for i, match in enumerate(self.finditer(string)):
            if count and i >= count:
                break
            result += string[pos:match.start()] + repl
            pos = match.end()
            substitutions += 1

        result += string[pos:]
        return result, substitutions

    def _update_pattern(self) -> None:

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

if __name__ == '__main__':
    print(Regex.count('b','abccbv'))
