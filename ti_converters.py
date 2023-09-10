import sys

if sys.platform == 'win32':
    from lib.dummy_types import *
    from lib.polyfill import is_numeric
else:
    from polyfill import is_numeric
    from dummy_types import *

from ti_formatters import PyFormatter, TiFormatter


def convert_element(x):
    if not isinstance(x, str):
        x = str(x)
        if "−" in x:
            x.replace("−", "-")
    if is_numeric(x):
        try:
            return int(x) if int(x) == float(x) else float(x)
        except ValueError:
            pass
    else:
        return x.strip('"\'')


class _ConversionAPI:
    def list(self):
        raise NotImplementedError("Subclasses must implement this method")

    def mat(self):
        raise NotImplementedError("Subclasses must implement this method")

    def row_vec(self):
        raise NotImplementedError("Subclasses must implement this method")

    def col_vec(self):
        raise NotImplementedError("Subclasses must implement this method")


class _Converter:
    @staticmethod
    def list(obj):
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def mat(obj):
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def row_vec(obj):
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def col_vec(obj):
        raise NotImplementedError("Subclasses must implement this method")


class _ConvertsToPy(_Converter):

    @staticmethod
    def _py_str_to_mat(ti_mat_str) -> list:
        if isinstance(ti_mat_str, list):
            return ti_mat_str

        if not TiCollections.is_py_mat_str(ti_mat_str):
            raise ValueError("Invalid ti matrix string: {}".format(ti_mat_str))
        return [
            [
                convert_element(x.strip()) for x in row.split(",")
            ]
            for row in ti_mat_str[2:-2].split("], [")
        ]

    @staticmethod
    def list(old_type):

        @staticmethod
        def from_py_str_list(obj) -> list:
            return [obj(x.strip()) for x in obj[1:-1].split(",")]

        def from_ti_mat(obj) -> list:
            # Convert a TI matrix string to a Python list
            return [item for sublist in obj for item in sublist]

        def from_ti_list(obj) -> list:
            # Convert a TI list string to a Python list
            return [x.strip() for x in obj[1:-1].split(",")]

        def from_py_mat(obj) -> list:
            # Convert a Python matrix to a Python list
            return [item for sublist in obj for item in sublist]

        conversion_mapping = {
            TiList: from_ti_list,
            TiMat: from_ti_mat,
            TiRowVec: from_ti_mat,
            TiColVec: from_ti_mat,
            PyMat: from_py_mat,
            PyStrList: from_py_str_list
        }

        if old_type in conversion_mapping:
            return conversion_mapping[old_type]

    @staticmethod
    def mat(old_type):
        pass

    @staticmethod
    def row_vec(old_type):
        pass

    @staticmethod
    def col_vec(old_type):
        pass


class _ConvertsToTi(_Converter):

    @staticmethod
    def ti_col_vec_from_py_col_vec(matrix):
        return _ConvertsToTi.to_ti_mat(matrix)

    @staticmethod
    def ti_list_from_py_list(py_list):
        return "{" + ",".join(map(str, py_list)) + "}"

    @staticmethod
    def ti_mat_from_py_mat(py_list):
        return "[" + "".join(map(lambda row: _ConvertsToTi.ti_list_from_py_list(row).replace('{', '[').replace('}', ']'), py_list)) + "]"

    @staticmethod
    def ti_row_vec_from_py_row_vec(matrix):
        return _ConvertsToTi.to_ti_mat(_ConvertsToTi.to_py_row_vec(matrix))

    @staticmethod
    def list(old_type):
        pass

    @staticmethod
    def mat(old_type):
        pass

    @staticmethod
    def row_vec(old_type):
        pass

    @staticmethod
    def col_vec(old_type):
        pass


class TiToPy(_ConversionAPI):
    @staticmethod
    def list(obj):
        converter, callback = PyFormatter.format_list(obj)
        converted = converter(obj)
        return callback(converted)

        if isinstance(obj, list):
            return obj
        elif TiCollections.is_ti_list(obj):
            return [obj(x.strip()) for x in obj[1:-1].split(",")]
        elif TiCollections.is_py_list_str(obj):
            return TiCollections.py_str_to_list(obj)
        raise UnconvertableString("Cannot convert to list: {}".format(obj))

    @staticmethod
    def mat(obj):
        if isinstance(obj, list):
            return obj
        if not TiCollections.is_ti_mat(obj):
            raise ValueError("Invalid ti matrix string: {}".format(obj))
        # Helper function to process a row string and return a list of processed elements

        def process_row(row_str):
            return [convert_element(x.strip().replace("−", "-")) for x in row_str.split(",")]
        # Remove outermost brackets and split the string into individual row strings
        row_strs = obj[2:-2].split("], [")
        # Process each row string and return the list of processed rows
        return [process_row(row_str) for row_str in row_strs]
        return TiCollections.to_py_mat(obj)

    @staticmethod
    def row_vec(obj):
        return TiCollections.to_py_row_vec(obj)

    @staticmethod
    def col_vec(obj):
        return TiCollections.to_py_col_vec(obj)


class PyToTi(_ConversionAPI):
    @staticmethod
    def list(obj):
        converter = TiFormatter.format_list(obj)
        converted = converter(obj)
        return converted

        if TiCollections.is_ti_list(py_list):
            return py_list
        return "{" + ",".join(map(str, py_list)) + "}"

    @staticmethod
    def mat(obj):
        pass

    @staticmethod
    def row_vec(obj):
        pass

    @staticmethod
    def col_vec(obj):
        pass
