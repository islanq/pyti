import sys
if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../'])

from polyfill import is_numeric, get_max_sequence, create_varied_sequence
from dummy_types import *

from collections import namedtuple
Dimensions = namedtuple('Dimensions', ['rows', 'cols'])


_comma_inclusive_variations = create_varied_sequence('],', '[', max=10)
_comma_exclusive_variations = create_varied_sequence(']', '[', max=10)


def seps_include_commas(x): return any(
    sep in x for sep in _comma_inclusive_variations)


def seps_exclude_commas(x): return any(
    sep in x for sep in _comma_exclusive_variations)


class _TypeTraits:
    def __init__(self, data: (list, str)) -> None:
        self._data = data.strip() if isinstance(data, str) else data
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
        return self.dim[0]

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


class _TiStringTraits(_TypeTraits):
    
    ti_type_mapping = {
        'col_vec': TiColVec,
        'row_vec': TiRowVec,
        'vec': TiVec,
        'mat': TiMat,
        'list': TiList
    }
    
    def __init__(self, string: str) -> None:
        super().__init__(string)

    def check_is_list(self) -> bool:
        if not isinstance(self.data, str):
            return False
        if not self.data.startswith('{'):
            return False
        if not self.data.endswith('}'):
            return False
        return not any(s in self.data for s in ['[', ':', ']'])

    def check_is_mat(self) -> bool:
        # ti mat will never contain ', ' or ':'
        if not isinstance(self.data, str):
            return False
        if seps_include_commas(self.data):
            return False
        if not self.data.startswith('[['):
            return False
        if not self.data.endswith(']]'):
            return False
        if ':' in self.data:
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
        return self.ti_type_mapping.get(self._weak_type, None)


class _PyStringTraits(_TypeTraits):
    
    ti_type_mapping = {
        'col_vec': TiColVec,
        'row_vec': TiRowVec,
        'vec': TiVec,
        'mat': TiMat,
        'list': TiList
    }
    
    def __init__(self, string) -> None:
        super().__init__(string)

    def check_is_list(self):
        if not isinstance(self.data, str):
            return False
        if seps_exclude_commas(self.data):
            return False
        # if re.match(_no_comma_seps, self.data):
        #     return False
        if not self.data.startswith("["):
            return False
        if not self.data.endswith("]"):
            return False
        # [1, 2, 3]
        return True

    def check_is_mat(self):
        if not isinstance(self.data, str):
            return False
        if seps_exclude_commas(self.data):
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
        # it must contain row separator
        # if not '], [' in self.data or not '],[' in self.data:
        if not seps_include_commas(self.data):
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
        return self.ti_type_mapping.get(self._weak_type, None)


class _PyTraits(_TypeTraits):
    
    py_type_mapping = {
        'col_vec': PyColVec,
        'row_vec': PyRowVec,
        'vec': PyVec,
        'mat': PyMat,
        'list': PyList
    }
    
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
        return self.py_type_mapping.get(self._weak_type, None)


class TraitsReport:

    _weights = {
        'list': 1,
        'mat': 2,
        'vec': 3,
        'col_vec': 4,
        'row_vec': 4  # assuming same particularity as col_vec
    }

    def __init__(self, obj: (str, list)) -> None:
        self.reports = [_PyTraits(obj), _PyStringTraits(
            obj), _TiStringTraits(obj)]
        self._valid_reports = [
            report for report in self.reports if report.is_valid]
        self._strongest = self._set_strongest()

    @property
    def has_valid(self):
        return self._has_valid

    @property
    def valid_count(self):
        return len(self._valid_reports)

    def all_reports(self):
        return self.reports

    def valid_reports(self):
        return self._valid_reports

    @property
    def has_strongest(self) -> bool:
        return self._strongest is not None

    @property
    def strongest(self) -> _TypeTraits:
        return self._set_strongest()

    def _set_strongest(self):
        # if self._strongest:
        #     return self._strongest
        if self.valid_count == 0:
            return None
        self._strongest = sorted(
            self._valid_reports, key=lambda x: self._weights[x.weak_type], reverse=True)[0]
        # self._strongest = next(report for report in self.reports if report.is_valid)
        return self._strongest

    @staticmethod
    def get_strongest(obj: (str, list)):
        return TraitsReport(obj).strongest


if __name__ == '__main__':
    
    
    pymat = [[1, "2x", 3], [4, 5, 6]]
    pycol = [[1], [2], [3]]
    pyrow = [[1, 2, 3]]
    pylst = [1, 2, 3]
    tilst = '{1, 2x, 3}'
    timat = '[[1, 2x, 3][4, 5, 6]]'
    ticol = '[[1][2][3]]'
    tirow = '[[1, 2, 3]]'

    pymat_report = TraitsReport.get_strongest(pymat)
    pylst_report = TraitsReport.get_strongest(pylst)
    tilst_report = TraitsReport.get_strongest(tilst)
    timat_report = TraitsReport.get_strongest(timat)
    pyrow_report = TraitsReport.get_strongest(pyrow)
    pycol_report = TraitsReport.get_strongest(pycol)
    ticol_report = TraitsReport.get_strongest(ticol)
    tirow_report = TraitsReport.get_strongest(tirow)

    assert(pymat_report.is_mat)
    assert(pylst_report.is_list)
    assert(tilst_report.is_list)
    assert(timat_report.is_mat)
    assert(pyrow_report.is_row_vec)
    assert(pycol_report.is_col_vec)
    assert(ticol_report.is_col_vec)
    assert(tirow_report.is_row_vec)
    
    assert(pymat_report.weak_type == 'mat')
    assert(pylst_report.weak_type == 'list')
    assert(tilst_report.weak_type == 'list')
    assert(timat_report.weak_type == 'mat')
    assert(pyrow_report.weak_type == 'row_vec')
    assert(pycol_report.weak_type == 'col_vec')
    assert(pycol_report.weak_type == 'col_vec')
    assert(pycol_report.weak_type == 'col_vec')
    assert(ticol_report.weak_type == 'col_vec')
    assert(tirow_report.weak_type == 'row_vec')
    
    
    assert(pymat_report.strong_type == PyMat)
    assert(pylst_report.strong_type == PyList)
    assert(tilst_report.strong_type == TiList)
    assert(timat_report.strong_type == TiMat)
    assert(pyrow_report.strong_type == PyRowVec)
    assert(pycol_report.strong_type == PyColVec)
    assert(ticol_report.strong_type == TiColVec)
    assert(tirow_report.strong_type == TiRowVec)
    
    print('all assertions passed')
