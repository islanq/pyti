import sys
if sys.platform == 'win32':
    exec(open('__init__.py').read())
    readST = None
    writeST = None
    eval_expr = None
    call_func = None
else: 
    from eval_expr import eval_expr, call_func  
    
def tiexec(cmd_str_or_func_name, *args):
    if len(args) > 0:
        try:
            return call_func(cmd_str_or_func_name, *args)
        except:
            pass
    try:
        return eval_expr(cmd_str_or_func_name)
    except:
        pass
    try:
        return readST(cmd_str_or_func_name)
    except:
        pass
    try:
        return readST('expr("{}")'.format(cmd_str_or_func_name))
    except:
        pass