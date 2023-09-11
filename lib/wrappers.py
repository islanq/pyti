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
            types_to_check = [type(args[i-1])
                              for i in indices]  # Indices are 1-based
            if len(set(types_to_check)) > 1:
                raise TypeError(
                    "Arguments at indices {} must be of the same type.".format(indices))
            return func(*args, **kwargs)
        return wrapper
    return decorator


def ensure_paired_type2(allowed_types):
    """
        @ensure_paired_type(allowed_types=[int])
        def do(one, two):
            return one + two

        do(1, 2)   # valid
        do(1, '2') # invalid

    """
    # Creating a wrapper function to ensure that the first two parameters are of specified types and match each other
    def decorator(func):
        def wrapper(arg1, arg2, *args, **kwargs):
            if type(arg1) not in allowed_types or type(arg2) not in allowed_types:
                raise TypeError(
                    "Arguments must be one of the allowed types: {}.".format(allowed_types))

            if type(arg1) != type(arg2):
                print("{} != {}".format(type(arg1), type(arg2)))
                raise TypeError("Arguments must be of the same type.")

            return func(arg1, arg2, *args, **kwargs)
        return wrapper
    return decorator


def ensure_paired_or_single_type2(allowed_types):
    # Extending the wrapper function to handle a single argument as well as paired arguments
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Handle the single argument case
            if len(args) == 1:
                if type(args[0]) not in allowed_types:
                    raise TypeError(
                        "The single argument must be one of the allowed types: {}.".format(allowed_types))

            # Handle the paired argument case
            elif len(args) >= 2:
                arg1, arg2 = args[:2]
                if type(arg1) not in allowed_types or type(arg2) not in allowed_types:
                    raise TypeError(
                        "Arguments must be one of the allowed types: {}.".format(allowed_types))

                if type(arg1) != type(arg2):
                    raise TypeError("Arguments must be of the same type.")

            else:
                raise TypeError(
                    "Insufficient number of arguments. At least one argument is required.")

            return func(*args, **kwargs)
        return wrapper
    return decorator


def ensure_single_or_paired_type(single_types, paired_type):
    """
    @ensure_single_or_paired_type(single_types=(int, str), paired_type=(list))
    def example_function(arg1, arg2=None):
        print("arg1: {}, arg2: {}".format(arg1, arg2))

    # Usage examples
    example_function(1)                   # Valid, single argument of type int
    example_function("hello")             # Valid, single argument of type str
    example_function([1, 2], [3, 4])      # Valid, paired arguments of type list
    example_function(1, "hello")          # Invalid, mixed types
    example_function([1, 2], "hello")     # Invalid, mixed types


    """
    # Extending the wrapper function to handle a single argument or paired arguments
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(args) == 1:
                if not isinstance(args[0], single_types):
                    raise TypeError(
                        "The single argument must be one of the allowed types: {}.".format(single_types))
            elif len(args) == 2:
                if not (isinstance(args[0], paired_type) and isinstance(args[1], paired_type)):
                    raise TypeError(
                        "Both arguments must be of type {}.".format(paired_type))
            else:
                raise TypeError(
                    "Invalid number of arguments. Must be either one or two arguments.")

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
                raise ValueError(
                    "index2 must be between 1 and {}.".format(len(matrix[0])))

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
                raise ValueError(
                    "index2 must be between 0 and {}.".format(max))

            return func(value, matrix, index1, index2, *args, **kwargs)
        return wrapper
    return decorator


def extends_method_names(cls):
    """
    Dynamically extend the class names on instantiation.

    Example:

    @extends_method_names
    class MyClass:

        def my_method(self):
            print("Hello")

    mc = MyClass()
    mc.mymethod()  # Prints "Hello"

    """
    for attr_name in dir(cls):
        if callable(getattr(cls, attr_name)) and '_' in attr_name:
            # Get the method
            method = getattr(cls, attr_name)

            # Create a new method name without underscores
            new_attr_name = attr_name.replace('_', '')

            # Check if the new attribute name already exists
            if not hasattr(cls, new_attr_name):
                # Set the method with the new name
                setattr(cls, new_attr_name, method)
    return cls


def ensure_paired_type(allowed_types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg in args[1:]:  # Skip the first argument which is the class reference 'cls'
                if not any(isinstance(arg, t) for t in allowed_types):
                    raise TypeError(
                        "Arguments must be one of the allowed types: {}.".format(allowed_types))
            return func(*args, **kwargs)
        return wrapper
    return decorator


def ensure_single_or_paired_type(single_types, paired_type):
    def decorator(func):
        def wrapper(*args):
            if len(args) == 2 and isinstance(args[1], single_types):
                pass
            elif len(args) == 3 and all(isinstance(arg, paired_type) for arg in args[1:]):
                pass
            else:
                raise TypeError(
                    "Invalid number of arguments. Must be either one or two arguments.")
            return func(*args)
        return wrapper
    return decorator
