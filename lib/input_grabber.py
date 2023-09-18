import sys
if sys.platform == 'win32':
    sys.path.extend(['../lib/', './lib/', '../', '.'])

from matrix_tools import convert_element
from ti_converters import parse_list

if sys.platform == 'win32':
    import os
    def clear(): return os.system('cls')
else:
    from ti_interop import clear


class InputGrabber:

    def __init__(self, initial_message="") -> None:
        self.initial_message = initial_message
        self.exit_request = False
        self.is_ok = None
        self.last_input = None
        if initial_message != "":
            print(initial_message)

    def clear(self):
        clear()

    def get_vectors(self, auto_clear=True) -> list:
        rows = None
        cols = None

        """
        Prompts the user to enter a matrix and returns the matrix as a list of lists
        """

        while rows is None or cols is None:
            try:
                if not rows:
                    row_input = convert_element(input('mat rows: '))
                    if row_input == 'q':
                        self.exit_request = True
                        return
                    if isinstance(row_input, int):
                        rows = row_input

                if not cols:
                    col_input = convert_element(input('mat cols: '))
                    if row_input == 'q':
                        self.exit_request = True
                        return
                    if isinstance(col_input, int):
                        cols = col_input
            except ValueError:
                print('Invalid input, please try again')

        vectors = []
        for i in range(rows):
            while True:
                row = input('Enter row {}: '.format(i+1))
                vector = parse_list(row)
                if len(vector) == cols:
                    break
                else:
                    print('Received {} elements, expected {}'.format(
                        len(vector), cols))
            vectors.append(vector)

        # clear on completion
        # if auto_clear:
        #     clear()

        return vectors

    def present_option(self, option_dialog: str, clear_on_resp=True, **kwargs):
        """ 
            Usage:
                self.present_option(valid_responses={'yes', 'no'}, callback=my_callback_function)
        """
        while True:
            try:
                resp = input(option_dialog)
                if resp == 'q' or resp == 'c':
                    self.exit_request = True
                    return
                self.last_input = resp

                if kwargs.get('valid_responses') and resp not in kwargs['valid_responses']:
                    raise ValueError("Invalid input")

                if kwargs.get('callback'):
                    if kwargs.get('pass_resp_to_callback', True):
                        kwargs['callback'](resp)
                    else:
                        kwargs['callback']()

                return resp
            except ValueError as e:
                print(e)
            finally:
                if clear_on_resp:
                    clear()

    def ask_yn_question(self, question):
        while True:
            try:
                resp = input(question).lower()
                if (resp == 'y' or resp == 'yes'):
                    return True
                elif (resp == 'n' or resp == 'no'):
                    return False
            except ValueError:
                print('Invalid input, please try again')
