import re
import sys
if sys.platform == 'win32':
    from lib.polyfill import is_numeric
    from lib.dummy_types import *
else:
    from polyfill import is_numeric
    from dummy_types import *

from ti_collections import UnconvertableString
from collections import namedtuple
from ti_converters import TiToPy
Dimensions = namedtuple('Dimensions', ['rows', 'cols'])

_no_comma_seps = re.compile(r'\b\]\s*\[\b')
_comma_seps = re.compile(r'\b\],\s*\[\b')


class _Traits:
    def __init__(self, data) -> None:
        self._data = data
        self._is_list = False
        self._is_mat = False
        self._is_vec = False
        self._is_col_vec = False
        self._is_row_vec = False
        self._is_valid = False
        self._weak_type = None
        self._strong_type = None
        self._validate()

    @property
    def data(self) -> any:
        return self._data

    @property
    def is_list(self) -> bool:
        return self._is_list

    @property
    def is_mat(self) -> bool:
        return self._is_mat

    @property
    def is_vec(self) -> bool:
        return self._is_vec

    @property
    def is_col_vec(self) -> bool:
        return self._is_col_vec

    @property
    def is_row_vec(self) -> bool:
        return self._is_row_vec

    @property
    def dim(self) -> Dimensions:
        return self._dim()

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def weak_type(self) -> str:
        return self._weak_type

    @property
    def strong_type(self) -> type:
        return self.deduce_type()

    def __len__(self) -> int:
        return self.dim.rows

    def check_is_list(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    def check_is_mat(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    def check_is_vec(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    def check_is_col_vec(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    def check_is_row_vec(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    def _dim(self) -> Dimensions:
        if not self._is_valid:
            return Dimensions(0, 0)
        if isinstance(self.data, str):
            return None
        if self._is_list and not self._is_mat:
            return Dimensions(len(self.data), 1)
        return None

    def _validate(self):
        self._is_list = self.check_is_list()
        self._is_mat = self.check_is_mat()
        self._is_vec = self.check_is_vec()
        self._is_col_vec = self.check_is_col_vec()
        self._is_row_vec = self.check_is_row_vec()

        self._is_valid = any([
            self._is_list,
            self._is_mat,
            self._is_vec,
            self._is_col_vec,
            self._is_row_vec
        ])

        if self.is_valid:
            if self.is_list:
                self._weak_type = 'list'
            if self.is_mat:
                self._weak_type = 'mat'
            if self.is_vec:
                self._weak_type = 'vec'
            if self.is_col_vec:
                self._weak_type = 'col_vec'
            if self.is_row_vec:
                self._weak_type = 'row_vec'
            if self.weak_type is None:
                return

            self._strong_type = self.deduce_type()

    def __str__(self) -> str:
        return str({
            'data': self.data,
            'is_list': self.is_list,
            'is_mat': self.is_mat,
            'is_vec': self.is_vec,
            'is_col_vec': self.is_col_vec,
            'is_row_vec': self.is_row_vec,
            'dim': self.dim,
            'is_valid': self.is_valid,
            'weak_type': self._weak_type,
            'strong_type': self._strong_type
        })

    def deduce_type(self):
        raise NotImplementedError("Subclasses must implement this method")


class TiStringTraits(_Traits):
    def __init__(self, string: str) -> None:
        super().__init__(string)

    def check_is_list(self) -> bool:
        if not isinstance(self.data, str):
            return False
        if not self.data.startswith('{'):
            return False
        if not self.data.endswith('}'):
            return False
        return all(s not in self.data for s in [', ', ':'])

    def check_is_mat(self) -> bool:
        # ti mat will never contain ', ' or ':'
        if not isinstance(self.data, str):
            return False
        if re.search(_comma_seps, self.data):
            print('comma seps re match')
            return False
        if not self.data.startswith('[['):
            return False
        if not self.data.endswith(']]'):
            return False
        if any(s in self.data for s in [':', '],[', '], [']):
            return False
        return True

    def check_is_vec(self) -> bool:
        return (self.check_is_row_vec()
                or self.check_is_col_vec())

    def check_is_col_vec(self) -> bool:
        # [[1][2][3]]
        # it is a ti mat
        if not self.check_is_mat():
            return False
        # it must contain row separator
        if not '][' in self.data:
            return False
        return not ',' in self.data

    def check_is_row_vec(self) -> bool:
        # [[1,2,3]]
        if not self.check_is_mat():
            return False
        if '][' in self.data:
            return False
        return ',' in self.data

    def _dim(self) -> Dimensions:
        dims = super()._dim()
        if dims:
            return dims
        try:
            # Check for the special case of an empty list of lists
            if self.data == "[[]]":
                return (1, 0)
            data = self.data.replace(' ', '')
            tokn = '],' if '],' in data else ']['
            # Split the string into rows
            rows = data[1:-1].split(tokn)

            # Find the number of rows and columns
            num_rows = len(rows)
            num_cols = len(rows[0][1:].split(','))

            return (num_rows, num_cols)
        except Exception:
            print('Error, unable to determine dimensions')
            return None

    def deduce_type(self):
        if self._weak_type == 'col_vec':
            return TiColVec
        if self._weak_type == 'row_vec':
            return TiRowVec
        if self._weak_type == 'mat':
            return TiMat
        if self._weak_type == 'list':
            return TiList
        if self._weak_type == 'vec':
            return TiVec
        return None


class PyStringTraits(_Traits):
    def __init__(self, string) -> None:
        super().__init__(string)

    def check_is_list(self):
        if not isinstance(self.data, str):
            return False
        if re.search(_no_comma_seps, self.data):
            return False
        if not self.data.startswith("["):
            return False
        if not self.data.endswith("]"):
            return False
        return True

    def check_is_mat(self):
        if not isinstance(self.data, str):
            return False
        if re.search(_no_comma_seps, self.data):
            return False
        if not self.data.startswith("[["):
            return False
        if not self.data.endswith("]]"):
            return False
        return True

    def check_is_vec(self):
        return self.check_is_col_vec() or self.check_is_row_vec()

    def check_is_col_vec(self):
        # [[1], [2], [3]]
        if not self.check_is_mat():
            return False
        # it must NOT contain row separator
        if not '], [' in self.data or not '],[' in self.data:
            return False
        if not self.dim:
            return False
        if self.dim.rows == 1:
            return False
        if self.dim.rows == self.dim.cols:
            return False
        if self.dim.cols == 1 and self.dim.rows > 1:
            return True
        return False

    def check_is_row_vec(self):
        # [[1,2,3]]
        if not self.check_is_mat():
            return False
        if any((s in self.data) for s in ['], [', '],[']):
            return False
        if not self.dim:
            return False
        if self.dim.cols == 1:
            return False
        if self.dim.rows == self.dim.cols:
            return False
        if self.dim.rows == 1 and self.dim.cols > 1:
            return True
        return False

    def _dim(self) -> Dimensions:
        dims = super()._dim()
        if dims:
            return dims
        try:
            # Check for the special case of an empty list of lists
            if self.data == "[[]]":
                return (1, 0)
            data = self.data.replace(' ', '')
            tokn = '],' if '],' in data else ']['
            # Split the string into rows
            rows = data[1:-1].split(tokn)

            # Find the number of rows and columns
            num_rows = len(rows)
            num_cols = len(rows[0][1:].split(','))

            return (num_rows, num_cols)
        except Exception:
            print('Error, unable to determine dimensions')
            return None

    def deduce_type(self):
        if self._weak_type == 'col_vec':
            return PyStrColVec
        if self._weak_type == 'row_vec':
            return PyStrRowVec
        if self._weak_type == 'vec':
            return PyStrVec
        if self._weak_type == 'mat':
            return PyStrMat
        if self._weak_type == 'list':
            return PyStrList
        return None


class PyTraits(_Traits):
    def __init__(self, object) -> None:
        super().__init__(object)

    def check_is_list(self) -> bool:
        return isinstance(self.data, list)

    def check_is_mat(self) -> bool:
        if not isinstance(self.data, list):  # it's not a list
            return False
        if len(self.data) == 0:  # it contains no rows, therefore not a matrix
            return False
        if not all(isinstance(row, list) for row in self.data):  # all list rows
            return False
        # all rows == len
        return all(len(row) == len(self.data[0]) for row in self.data)

    def check_is_vec(self) -> bool:
        return (self.check_is_row_vec()
                or self.check_is_col_vec())

    def check_is_col_vec(self) -> bool:
        if not isinstance(self.data, list):
            return False
        return all(isinstance(row, list)
                   and len(row) == 1 for row in self.data)

    def check_is_row_vec(self) -> bool:
        if isinstance(self.data, list):
            return len(self.data) == 1 and isinstance(self.data[0], list)
        return False

    def _dim(self) -> Dimensions:
        dims = super()._dim()
        if dims:
            return dims
        return Dimensions(len(self.data), len(self.data[0]))

    def deduce_type(self):
        if self._weak_type == 'row_vec':
            return PyRowVec
        if self._weak_type == 'col_vec':
            return PyColVec
        if self._weak_type == 'vec':
            return PyVec
        if self._weak_type == 'mat':
            return PyMat
        if self._weak_type == 'list':
            return PyList
        return None


def get_report(obj: (str, list), strict=False):
    def strongest_compatibility(reports):
        # Assign weights
        weights = {
            'list': 1,
            'mat': 2,
            'vec': 3,
            'col_vec': 4,
            'row_vec': 4  # assuming same particularity as col_vec
        }

        # Filter valid reports
        valid_reports = [report for report in reports if report['is_valid']]

        # Sort based on weights
        sorted_reports = sorted(
            valid_reports, key=lambda x: weights[x['weak_type']], reverse=True)

        # The first report in the sorted list is the strongest compatibility
        return sorted_reports[0]

    reports = [PyTraits(obj), PyStringTraits(obj), TiStringTraits(obj)]
    if sum(report.is_valid for report in reports) > 1:
        return strongest_compatibility(reports)
    return next(report for report in reports if report.is_valid)
