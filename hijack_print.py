_original_print = print  # Save the original print function

class CapturePrint:
    def __init__(self):
        self.buffer = []

    def __enter__(self):
        global print  # Declare print as global to override it
        def custom_print(*args, **kwargs):
            self.buffer.append(' '.join(map(str, args)))  # Append to the buffer
        print = custom_print  # Override the print function
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global print
        print = _original_print  # Restore the original print function

    def getvalue(self):
        return '\n'.join(self.buffer)
      
"""
    # Usage:
    with CapturePrint() as c:
        print("This is captured!")
        print("This too!")

    output = c.getvalue()
    _original_print("Captured output:", output)
"""
