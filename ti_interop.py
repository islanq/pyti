import sys
if sys.platform == 'win32':
    exec(open('__init__.py').read())
    readST = None
    writeST = None
    eval_expr = None
    call_func = None
else: 
    from eval_expr import eval_expr, call_func
    from ti_system import readST, writeST
    
_assignment_operators =[':=', '→']
    
class TiType:
    pass

class TiUninitializedVariableError(NameError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

def _string_all_args(*args):
    lst = []
    for arg in args:
        if isinstance(arg, str):
            lst.append(arg)
        else:
            lst.append(str(arg))
    return ", ".join(lst)

    
def tiexec(cmd_str_or_func_name, *args, write=False):
    if write:
        try:
            writeST(cmd_str_or_func_name, *args)
            return
        except TiUninitializedVariableError as err:
            pass
    if len(args) > 0:
        try:
            return call_func(cmd_str_or_func_name, *args)
        except TiUninitializedVariableError as err:
            pass
    if _is_assignment_attempt(cmd_str_or_func_name):
        do_manual_assignment(cmd_str_or_func_name)
        return

    try:
        return eval_expr(cmd_str_or_func_name)
    except TiUninitializedVariableError as err:
        pass
    try:
        return readST(cmd_str_or_func_name)
    except TiUninitializedVariableError as err:
        pass
    try:
        return readST('expr("{}")'.format(cmd_str_or_func_name))
    except TiUninitializedVariableError as err:
        pass
    
def _is_assignment_attempt(expr):
    return any(op in expr for op in _assignment_operators)

def var_save(name, value):
    try:
        writeST(name, value)
    except:
        pass

def clearAZ():
    for c in range(97, 122):
        if get_var(chr(c)) is not None:
            del_var(chr(c))
    
def var_exists(name):
    return get_var(name) is not None

def get_var(name):
    try:
        return readST("{}".format(name))
    except Exception:
        return None
    
def del_var(*names):
    for name in names:
        name = str(name) if not isinstance(name, str) else name
        had_var = get_var(name) is not None
        try:
            if had_var:
                readST("delvar {}".format(name))
            else:
                writeST(name, "none")
                return del_var(name)
        except Exception as err:
            if had_var:
                return had_var
            else:
                print("del_var had an error it couldn't resolve: {}".format(err))
                return False
            
def do_manual_assignment(command):
    if _assignment_operators[0] in command:
        lhs, rhs = command.split(_assignment_operators[0])
    else:
        rhs, lhs = command.split(_assignment_operators[1])
    del_var(lhs.strip())
    return var_save(lhs.strip(), rhs.strip())