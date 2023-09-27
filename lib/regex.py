from cachable import Cachable as _Cachable
from collections import namedtuple as _namedtuple
from adt import AbstractDataType
import re as _re
import sys

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
        elif (isinstance(start, int)
         and isinstance(end, int)):
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
    def __init__(self, match, start: int, end: int, bypass  = False, string= None) -> None:
        
        if bypass:
          
            self._span = (Span(match.span()),)
            self._groups = match.groups()
            self._group = [(match.group(x)) for x in range(len(match.regs))]
            self.string = match.string
            return
        
        
        self._span = (Span(start, end),)
        self._groups = ()
        self._group = ()
        if string:
            self.string = string
        

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
        return "<rx.Match object; span=({}, {}), match='{}'>".format(self.start(), self.end(), self.string[self.span().start:self.span().end])

    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return len(self._span)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Match):
            return (self._span   == __value._span 
                and self.string  == __value.string)
        elif isinstance(__value, _re.Match):
            return (self.start() == __value.start()
                and self.end()   == __value.end()   
                and self.string  == __value.string)
        else:
            raise TypeError('Invalid argument type')


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

    def __init__(self, pattern, flags: RegexFlags = RegexFlags.NONE, force=False) -> None:

        self._fullenv = sys.implementation.name != 'micropython'
        self._forced = force   # force the use of custom implementation
        self._patstr = pattern # the pattern string
        self._flags = flags    # the pattern flags
        self._refresh = True   # refresh the pattern

        self._re_search = None # the re search method
        self._re_match = None  # the re match method

        self._update_pattern()

        if self._forced and self._fullenv:
            self._fullenv = False

    @property
    def flags(self):
        return self._flags

    @property
    def pattern(self):
        return self._re_pat

    def match(self, string: str, start: int = 0, end: int = None, omit_positions: bool = False) -> Match | None:
        """Implements the match method using re.match."""
        return self._find(self.pattern.match, string, start, end, omit_positions)

    def count(self, string: str, start: int = 0, end: int = None) -> int:
        """Implements the count method using custom implementation."""
        return len(self.findall(string, start, end))

    def search(self, string: str, start: int = 0, end: int = None, omit_positions: bool = False) -> Match | None:
        return self._find(self.pattern.search, string, start, end, omit_positions)

    def _find(self, method: callable, string: str, start: int = 0, end: int = None, omit_positions: bool = False) -> Match:
        # set the end to the length of the string if not provided
        if end is None:
            end = len(string)

        # trim the string down before searching
        match = method(string[start:end])
        if not match:
            return None
        
        # if we are in a full python environment,
        # we can use the re span and bypass processing 
        # so we'll just return the original re match
        if self._fullenv and not self._forced:
            return match
                
        if omit_positions:
            return Match(match, None, None)

        return self._process_match(match, string, start, end)

    def findall(self, string: str, start: int = 0, end: int = None) -> list[str]:
        return [m.string[m.span().start : m.span().end] for m in self.finditer(string, start, end)]

    def split(self, string: str, maxsplit: int = 0, start: int = 0, end: int = None) -> list[str]:
        
        matches = self.sub('/\\', string, maxsplit).split('/\\')
        return [string] if matches is None else matches 
        
        
    def finditer(self, string: str, start: int = 0, end=None):
        """Implements the finditer method using custom implementation."""
        if end is None:
            end = len(string)
            
        # we have a full env and are not forcing the custom implementation
        if self._fullenv and not self._forced:
            for match in self._re_pat.finditer(string[start:end]):
                yield Match(match, start, end, True)
            return

        pos = start
        idx = 0
        # while we have matches
        while True:

            match = self.search(string, pos, end)

            if not match:
                break
            """
                Populating the span objects:
                
                Micro Env:
                
                (1) In a micro env we call self.search
                (2) self.search calls self._find, which 
                (3) self._find calls self._process_match
                (4) process match populates our span object
                
                
                Process Matche's span creating behavior:
                --------------------------------------------
                Our span object, unlike the true span object,
                will be not be the absolute position of the match,
                but rather the position of the match relative
                to the start of the string
                
                1) process match checks group 0, which is the entire match
                2) it then finds the index of the match in the string using find
                    a. find will return the first index of the match
                3) process match uses first found index + the length of the match
                
                Conclusion:
                --------------------------------------------------
                This means we have to compute the absolute position of the match
                relative to the start of the string, and then use that to create
                
                Example:
                --------------------------------------------------
                let's search for 'i' in 'this is a string'
            
                iter|  0123456789012345  |fspan|mlen| pos |native re
                ----|--------------------|--------------------------
                 1  | 'this is a string' |     |    |   0 | 
                    |  >>^               |(2,3)| 1  | 2+1 |(2,3)
                 2  | 's is a string'    |     |    | = 3 |
                    |  >>^               |(2,3)| 1  | 2+1 |(5,6)
                 3  | 's a string'       |     |    | = 6 |
                    |  >>>>>>>^          |(7,8)| 1  | 7+1 |(13,14)
                 4  | 'ng'               |     |    | =14 |
                    |  >>                |None |    |     |
                    
            """
            
            
            
            beg_span = match.span(0).start + pos
            end_span = match.span(0).end + pos
            
            if idx != 0:
                end_span - len(match.group(0))
                
            idx += 1
            pos += match.start() + len(match)
            
            match.span(0, Span(beg_span, end_span))
            
            yield match

    def _process_match(self, match, string: str, start: int, end: int):
        if self._fullenv:
            # This will work in full Python environments
            # but we should have bypassed this method
            # so this is just for testing
            span = match.span()
            beg = start + span[0]
            end = start + span[1]
        else:
            # In MicroPython environment, find start and end positions using a custom method
            beg = string[start:end].index(match.group(0))
            end = beg + len(match.group(0))
            
        return Match(match, beg, end, string=string)

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

        restr = self._patstr
        flags = self._flags

        try:
            self._re_pat = _re.compile(restr, flags)
            self._re_search = self._re_pat.search
            self._re_match = self._re_pat.match
        except _re.error:
            print('Invalid pattern')

        self._refresh = False


if __name__ == '__main__':
    
    string = 'this is a test string'
    pattern = 'th|is'
    methods = (Pattern(pattern, 0), Pattern(pattern, 0, True))
    pass_message = lambda name: print('{} assertions passed!'.format(name))
    
    def test_match():
        for method in methods:
            result = method.match(string)
            match  = _re.match(pattern, string)
            #
            assert match.group(0) == result.group(0)
            assert match.span() == result.span()
            assert match.start() == result.start()
            assert match.end() == result.end()
            assert match.string == result.string
    
    def test_search():
        for method in methods:
            result = method.search(string)
            search = _re.search(pattern, string)
            #
            assert search.group(0) == result.group(0)
            assert search.span() == result.span()
            assert search.start() == result.start()
            assert search.end() == result.end()
            assert search.string == result.string
        pass_message('Search')

    def test_findall():
        for method in methods:
            result = method.findall(string)
            assert _re.findall(pattern, string) == result
        pass_message('Findall')
    
    def test_split():
        for method in methods:
            result = method.split(string)
            relist = _re.split(pattern, string)
            #
            assert len(relist) == len(result)
            assert relist == result
            
        pass_message('Split')
    
    def test_finditer():
        for method in methods:
            result = list(method.finditer(string))
            relist = list(_re.finditer(pattern, string))
            #
            assert len(result) == len(relist)
            assert result[0].group(0) == relist[0].group(0)
            assert result[0].span() == relist[0].span()
        pass_message('Finditer')
        
    test_match()
    test_search()
    test_findall()
    test_split()
    test_finditer()
