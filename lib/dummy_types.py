class TiType:
    def __init__(self, data: str):
        self.data = data

class TiList(TiType):
    def __init__(self, data):
        super().__init__(data)

class TiMat(TiType):
    def __init__(self, data):
        super().__init__(data)

class TiVec(TiType):
    def __init__(self, data):
        super().__init__(data) 


class TiColVec(TiVec):
    def __init__(self, data):
        super().__init__(data)


class TiRowVec(TiVec):
    def __init__(self, data):
        super().__init__(data)


class PyType:
    def __init__(self, data: list):
        self.data = data


class PyList(PyType):
    def __init__(self, data):
        super().__init__(data)


class PyMat(PyType):
    def __init__(self, data):
        super().__init__(data)


class PyVec(PyType):
    def __init__(self, data: list):
        super().__init__(data)


class PyColVec(PyVec):
    def __init__(self, data):
        super().__init__(data)


class PyRowVec(PyVec):
    def __init__(self, data):
        super().__init__(data)


class PyStrType:
    def __init__(self, data: str):
        super().__init__(data)


class PyStrList(PyStrType):
    def __init__(self, data: str):
        super().__init__(data)


class PyStrMat(PyStrType):
    def __init__(self, data: str):
        super().__init__(data)


class PyStrVec(PyStrType):
    def __init__(self, data: str):
        super().__init__(data)


class PyStrColVec(PyStrVec):
    def __init__(self, data):
        super().__init__(data)


class PyStrRowVec(PyStrVec):
    def __init__(self, data):
        super().__init__(data)
