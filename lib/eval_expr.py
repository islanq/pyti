def _add_required_local_func():
    func_str =   'Define strsub(s,so,sn)=Func'
    func_str += ':Local c,sl'
    func_str += ':""→sl'
    func_str += ':inString(s,so)→c'
    func_str += ':While c>0'
    func_str += ':  sl&mid(s,1,c-1)&sn→sl'
    func_str += ':  mid(s,c+dim(so))→s'
    func_str += ':  inString(s,so)→c'
    func_str += ':EndWhile'
    func_str += ':Return sl&s'
    func_str += ':EndFunc'
    funs = None
    from ti_system import readST
    try:
        funs = readST('getvarinfo()')
    except:
        pass
    if not "strsub" in funs:
        try:
            readST( func_str)
        except:
            pass

# Internal helper functions....
def _return_number_if_possible(s):
    try:
        f = float(s)
        return int(f) if int(f) == f else f
    except ValueError:
        return s

def _return_evaled_if_possible(thing):
    try:
        return eval("("+str(thing)+")")
    except:
        return thing

def _cleanstr(res):
    res = res[1:-1]  # to remove the quotes
    res = res.replace("*\uf02f", "j")  # complex i
    res = res.replace("\uf02f", "j")  # complex i
    res = res.replace("\u221a", "sqrt")
    res = res.replace("\u03c0", "pi")
    res = res.replace("\uf03f", "e")
    res = _return_number_if_possible(res)  # auto type...
    return res

# Public functions
def eval_expr(expr, trypyeval=False):
    from ti_system import writeST, readST
    try:
        writeST("tmppy_", 'strsub(string(' + str(expr) + '),"/","$%$")')  # eval and store
        res = readST("tmppy_")  # retrieve stored value
        res = res.replace("$%$", "/")  # magic replacement
        res = _cleanstr(res)
        if trypyeval == True:
            res = _return_evaled_if_possible(res)
        return res
    except Exception as err:
        print(err)
        return res

def call_func(funcname, *pyargs):
    fargs = ','.join(map(str, pyargs))
    expr = funcname + '(' + fargs + ')'
    try:
        res = eval_expr(expr)
        return res if res != expr else None
    except Exception as err:
        print("Something went wrong...\nres: {}\nerror:{}".format(res, err))
        return None

# Aliases for compat with other stuff
caseval = eval_expr
eval_native = eval_expr
# dynamically add the required local func
# becuase if it's not defined, we will throw
# errors while trying to eval
_add_required_local_func()