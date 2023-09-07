def ensure_same_type(func):
    '''Ensure that the first two arguments to the function are of the same type.'''
    def wrapper(param1, param2, *args, **kwargs):
        if type(param1) != type(param2):
            raise TypeError("The types of param1 and param2 must be the same.")
        return func(param1, param2, *args, **kwargs)
    return wrapper

def ensure_all_same_type(func):
    '''Ensure that all arguments to the function are of the same type.'''
    def wrapper(*args, **kwargs):
        types = {type(arg) for arg in args}
        if len(types) > 1:
            raise TypeError("All arguments must be of the same type.")
        return func(*args, **kwargs)
    return wrapper

def ensure_same_type_index(*indices):
    '''Ensure that the arguments at the given indices are of the same type.'''
    def decorator(func):
        def wrapper(*args, **kwargs):
            types_to_check = [type(args[i-1]) for i in indices]  # Indices are 1-based
            if len(set(types_to_check)) > 1:
                raise TypeError("Arguments at indices {} must be of the same type.".format(indices))
            return func(*args, **kwargs)
        return wrapper
    return decorator

def ensure_paired_type(allowed_types):
    # Creating a wrapper function to ensure that the first two parameters are of specified types and match each other
    def decorator(func):
        def wrapper(arg1, arg2, *args, **kwargs):
            if type(arg1) not in allowed_types or type(arg2) not in allowed_types:
                raise TypeError("Arguments must be one of the allowed types: {}.".format(allowed_types))
            
            if type(arg1) != type(arg2):
                print("{} != {}".format(type(arg1), type(arg2)))
                raise TypeError("Arguments must be of the same type.")
                
            return func(arg1, arg2, *args, **kwargs)
        return wrapper
    return decorator

def ensure_paired_or_single_type(allowed_types):
    # Extending the wrapper function to handle a single argument as well as paired arguments
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Handle the single argument case
            if len(args) == 1:
                if type(args[0]) not in allowed_types:
                    raise TypeError("The single argument must be one of the allowed types: {}.".format(allowed_types))
            
            # Handle the paired argument case
            elif len(args) >= 2:
                arg1, arg2 = args[:2]
                if type(arg1) not in allowed_types or type(arg2) not in allowed_types:
                    raise TypeError("Arguments must be one of the allowed types: {}.".format(allowed_types))
                
                if type(arg1) != type(arg2):
                    raise TypeError("Arguments must be of the same type.")
            
            else:
                raise TypeError("Insufficient number of arguments. At least one argument is required.")
                
            return func(*args, **kwargs)
        return wrapper
    return decorator



def validate_one_based_indices():
    def decorator(func):
        def wrapper(value, matrix, index1, index2, *args, **kwargs):
            # Check if index1 and index2 are integers
            if not isinstance(index1, int) or not isinstance(index2, int):
                raise TypeError("Both index1 and index2 must be integers.")
            
            # Check if index1 is > 0
            if index1 <= 0:
                raise ValueError("index1 must be greater than 0.")
                
            # Check if index2 <= len(matrix[0])
            if index2 > len(matrix[0]) or index2 <= 0:
                raise ValueError("index2 must be between 1 and {}.".format(len(matrix[0])))
            
            return func(value, matrix, index1, index2, *args, **kwargs)
        return wrapper
    return decorator

def validate_zero_based_indices():
    def decorator(func):
        def wrapper(value, matrix, index1, index2, *args, **kwargs):
            # Check if index1 and index2 are integers
            if not isinstance(index1, int) or not isinstance(index2, int):
                raise TypeError("Both index1 and index2 must be integers.")
            

            max = len(matrix[0]) - 1
            # Check if index1 is > 0
            if index1 < 0:
                raise ValueError("index1 must be >=  0.")
                
            # Check if index2 <= len(matrix[0])
            if index2 >= max or index2 <= 0:
                raise ValueError("index2 must be between 0 and {}.".format(max))
            
            return func(value, matrix, index1, index2, *args, **kwargs)
        return wrapper
    return decorator