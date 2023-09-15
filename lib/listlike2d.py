from collections import namedtuple
from matrix_tools import flatten, convert_element, is_flat_list
from ti_formatting import mat_repr, display_matrix
Dimensions = namedtuple('Dimensions', ['rows', 'cols'])


class ListLike2D:


    def __init__(self, data, cols = None, fill = 0) -> None:
        
        # we are specifying the number of rows and cols
        # and populating the matrix with the fill value
        if isinstance(data, int) and isinstance(cols, int):
            self.data = [[fill] * cols for _ in range(data)]
        elif isinstance(data, list) and isinstance(cols, int):
            
            lst = flatten(data)
            length = len(lst)
            
            if length % cols == 0:
                iters = length // cols
            else:
                iters = length // cols + 1
                
            self.data = []
            
            for i in range(iters):
                row = []
                for j in range(cols):
                    index = i * cols + j
                    if index < length:
                        elem = convert_element(lst[index])
                        row.append(elem)
                    else:
                        row.append(fill)
                self.data.append(row)
                
        elif isinstance(data, int) and not cols:
            raise ValueError("If data is an int, cols must be specified")
        elif isinstance(data, list) and not cols:
            if len(data) == 0:
                raise ValueError("data must be a non-empty list")
            if not isinstance(data[0], list):
                self.data = [data]
            # all rows must be the same length
            elif not all(len(row) == len(data[0]) for row in data):
                raise ValueError("All rows must be the same length")
            else:
                self.data = data
        
        # convert all elements to numeric if possible
        for row in self.data:
            for i in range(len(row)):
                row[i] = convert_element(row[i])
                
        self._dims = None
        self._current = 0


#region properties

    @property
    def dims(self) -> Dimensions:
        if self._dims is None:
            self._set_dims()
        return self._dims


    @property
    def is_vector(self) -> bool:
        return self.dims.cols == 1 or self.dims.rows == 1


    @property
    def is_row_vector(self) -> bool:
        return self.dims.rows == 1


    @property
    def is_matrix(self) -> bool:
        return not self.is_vector and self.dims.rows > 1 and self.dims.cols > 1 


    @property
    def is_col_vector(self) -> bool:
        return self.dims.cols == 1

#endregion properties


#region dunder methods

    def __eq__(self, other: object) -> bool:
        if isinstance(other, list):
            return self.data == other
        if not hasattr(other, 'data'):
            return False
        if not isinstance(other.data, list):
            return False
        return self.data == other.data


    def __len__(self) -> int:
        return len(self.data)

    
    def __getitem__(self, indices: (tuple,int)) -> any:
        if isinstance(indices, tuple):
            return self.data[indices[0]][indices[1]]
        if isinstance(indices, int):
            return self.data[indices]
        raise TypeError("indices must be an int or a tuple of ints")


    def __setitem__(self, indices: (tuple, int), value: any) -> None:
        if isinstance(indices, tuple):
            self.data[indices[0]][indices[1]] = value
        elif isinstance(indices, int):
            self.data[indices] = value
        raise TypeError("indices must be an int or a tuple of ints")


    def __iter__(self) -> 'ListLike2D':
        self._current = 0
        return self


    def __next__(self) -> any:
        if self._current >= len(self):
            raise StopIteration
        
        item = self[self._current]
        self._current += 1
        return item


    def __list__(self) -> list:
        return self.data
    

    def __str__(self) -> str:
        return mat_repr(self.data)


    def __repr__(self) -> str:
        return mat_repr(self.data)


#endregion dunder methods

        
    def clone_data(self) -> list:
        """_summary_ returns a copy of the internal data structure.
        Returns:
            _type_: _description_
        """
        return [row[:] for row in self.data]
    
        
    def clone(self) -> 'ListLike2D':
        """_summary_ returns a copy of the matrix
        of the internal data structure.

        Returns:
            _type_: _description_
        """
        return ListLike2D(self.data)


    def T(self, count: int = 1) -> 'ListLike2D':
        for _ in range(count):
            self.transpose()
        return self


    def set_column(self, col: int, values: list) -> None:
        if len(values) != self.dims.rows:
            raise ValueError("values must have length {}".format(self.dims.rows))
        values = flatten(values)
        for row in range(self.dims.rows):
            
            self.data[row][col] = values[row]
        return self


    def set_row(self, row: int, values: list) -> 'ListLike2D':
        if len(values) != self.dims.cols:
            raise ValueError("values must have length {}".format(self.dims.cols))
        self.data[row] = values
        return self


    def _set_dims(self) -> None:
        self._dims = Dimensions(len(self.data), len(self.data[0]))
   

    def _flatten(self):
        self.data = flatten(self.data)
        self._set_dims()
        return self


    def append(self, list_like):
        """
            Will try to append a row or column vector to the matrix 
            based on the shape of the list_like object
        """
        if isinstance(list_like, list):
            list_like = ListLike2D(list_like)
        if not isinstance(list_like, ListLike2D):
            raise TypeError("list_like must be a list or ListLike2D")
        if list_like.is_vector:
            self.append_col(list_like.data)
        else:
            self.append_row(list_like.data)
            

    def append_row(self, row: list):
        # if row is a list of lists, flatten it
        if hasattr(row, 'data'):
            row = row.data
        if not isinstance(row, list):
            raise TypeError("row must be a list or ListLike2D")
        row = flatten(row)
        # ensure row is a list
        if len(row) != self.dims.cols:
            raise ValueError("row must have length {}".format(self.dims.cols))
        self.data.append(row)
        self._set_dims()
        return self


    def append_col(self, col: list):
        # if col is a list of lists, flatten it
        if hasattr(col, 'data'):
            col = col.data
        if not isinstance(col, list):
            raise TypeError("row must be a list or ListLike2D")
        col = flatten(col)
        # ensure col is a list
        if len(col) != self.dims.rows:
            raise ValueError("col must have length {}".format(self.dims.rows))
        for i in range(self.dims.rows):
            self.data[i].append(col[i])
        self._set_dims()
        return self
      
        
    def reshape(self, rows: int = None, cols: int = None, fill: int = 0) -> None:
        # Flatten the data
        data = flatten(self.data)
        
        # Determine new dimensions
        if rows is not None and cols is None:
            cols = len(data) // rows + (1 if len(data) % rows != 0 else 0)
        elif cols is not None and rows is None:
            rows = len(data) // cols + (1 if len(data) % cols != 0 else 0)
        elif rows is not None and cols is not None:
            if rows * cols < len(data):
                raise ValueError("rows * cols must be greater than or equal to the number of elements in the matrix")
        else:
            raise ValueError("Either rows or cols must be specified")
        
        # Reshape the data
        self.data = []
        for i in range(rows):
            row = []
            for j in range(cols):
                index = i * cols + j
                if index >= len(data):
                    row.append(fill)
                else:
                    row.append(data[index])
            self.data.append(row)
        
        # Set the new dimensions
        self._set_dims()
        return self


    def transpose(self):
        # swap rows and columns
        data = [[self.data[j][i] for j in range(self.dims.rows)] for i in range(self.dims.cols)]
        self.data = data
        self._set_dims()
        return self


    def get_cols(self, *cols):
        # return the specific column
        if len(cols) == 1 and isinstance(cols[0], int):
            return ListLike2D([self.data[i][cols[0]] for i in range(self.dims.rows)]).T()
        if all(isinstance(col, int) for col in cols):
            return ListLike2D([[self.data[i][col] for col in cols] for i in range(self.dims.rows)]).T(2)


    def get_rows(self, *rows):
        if len (rows) == 1 and isinstance(rows[0], int):
            return ListLike2D(self.data[rows[0]])
        if all(isinstance(row, int) for row in rows):
            return ListLike2D([self.data[row] for row in rows])


    def shift_left(self, insert=False):
        new_data = [row[1:] + [row[0]] for row in self.data]
        if insert:
            for row in new_data:
                row.append(0)
        self.data = new_data
        self._set_dims()
        return self


    def shift_up(self, insert=False):
        new_data = [self.data[i - 1] for i in range(len(self.data))]
        if insert:
            new_data.append([0] * len(self.data[0]))
        self.data = new_data
        self._set_dims()
        return self


    def shift_down(self, insert=False):
        new_data = [self.data[(i + 1) % len(self.data)] for i in range(len(self.data))]
        if insert:
            new_data.insert(0, [0] * len(self.data[0]))
        self.data = new_data
        self._set_dims()
        return self


    def shift_right(self, insert=False):
        rows, cols = self.dims
        
        # Shifting each row to the right by one position
        new_data = [[row[-1]] + row[:-1] for row in self.data]
        
        # Inserting a new column of zeros at the beginning if insert is True
        if insert:
            for row in new_data:
                row.insert(0, 0)
        
        # Updating the data attribute with the new data
        self.data = new_data
        self._set_dims()
        return self


    def swap_rows(self, row1, row2):
        if row1 < 0 or row1 >= self.dims.rows:
            raise ValueError("row1 must be between 0 and {}".format(self.dims.rows - 1))
        self.data[row1], self.data[row2] = self.data[row2], self.data[row1]
        return self


    def swap_columns(self, col1, col2):
        if col1 < 0 or col1 >= self.dims.cols:
            raise ValueError("col1 must be between 0 and {}".format(self.dims.cols - 1))
        if col1 == col2:
            return self
        for row in self.data:
            row[col1], row[col2] = row[col2], row[col1]
        return self    
 
    
# ll = ListLike2D([
#     [1,2,3],
#     [4,5,6],
#     [7,8,9]
# ])




# print(ll.swap_columns(0, 2))
