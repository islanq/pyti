from ti_interop import tiexec
from ti_collections import TiCollections as TiCollections
from ti_matrix import TiMatrix
from wrappers import extends_method_names


@extends_method_names
class TiList(TiCollections):

    def __init__(self, list_or_str: (str, list) = None, *args):
        if list_or_str is None:
            list_or_str = []
        if not isinstance(list_or_str, list):
            list_or_str = [list_or_str]

        if len(args) > 0 and isinstance(args[0], list):
            list_or_str.extend(args[0])
        elif len(args) > 0:
            list_or_str.extend(list(args))

        self.ti_list = self.to_ti_list(list_or_str)
        self.py_list = self.to_py_list(self.ti_list)

        self.data = self.py_list
        self.index = 0

    def is_ti_list(self, ti_list_str) -> bool:
        if not isinstance(ti_list_str, str):
            return False
        return TiCollections.is_ti_list(ti_list_str)

    def __getitem__(self, index):
        return self.py_list[index]

    def __len__(self) -> int:
        return len(self.py_list)

    def dim(self) -> int:
        return int(tiexec("dim({})".format(self.ti_list)))

    def __list__(self) -> list:
        return self.py_list

    def __TiMatrix__(self):
        return TiCollections.to_py_mat(self.ti_list)

    def to_ti_mat(self, elements_per_row=1) -> TiMatrix:
        return TiMatrix(tiexec("list@>mat({},{})".format(self.ti_list, elements_per_row)))

    def to_ti_col_vec(self, elements_per_row=1) -> str:
        return TiMatrix(self.to_ti_mat(elements_per_row))

    def to_ti_row_vec(self) -> str:
        return TiMatrix(self.to_ti_mat(len(self)))

    def __iter__(self):
        # The iterator object should be the instance itself
        return self

    def __next__(self):
        if self.index < len(self.data):
            value = self.data[self.index]
            self.index += 1
            return value
        else:
            # Raise StopIteration to signal the end of iteration
            raise StopIteration

    def __repr__(self) -> str:
        return str(self.py_list)

    def __str__(self) -> str:
        return str(self.py_list)
