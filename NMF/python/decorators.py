class selfType(object):
    pass

def Self():
    return type(selfType)

def accepts(*types):
    def check_accepts(f):
        assert len(types) == f.func_code.co_argcount
        def new_f(*args, **kwds):            
            for (a, t) in zip(args, types):  
                assert ((t == type(selfType)) or isinstance(a, t)), "arg %r does not match %s" % (a,t)
            return f(*args, **kwds)
        new_f.func_name = f.func_name
        return new_f
    return check_accepts

#checks only first layer
def returns(rtype):
    def check_returns(f):  
        def new_f(*args, **kwds):
            r = f(*args, **kwds)
            if (rtype != None and r == None):
                print("ERROR: Returning None even though it's not technically allowed! This may lead to further errors.")
            assert ((rtype == type(selfType)) or r == None or isinstance(r, rtype)), "return type does not match decorator"
            return r        
        new_f.func_name = f.func_name
        return new_f
    return check_returns

