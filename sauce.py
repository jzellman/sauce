import web
import types

class application(web.application):
    urls = {}
    def handle(self):
        method = web.ctx.method
        application.urls[method]
        fn, args = self._match(application.urls[method], web.ctx.path)
        return self._delegate(fn, self.fvars, args)

    def _delegate(self, fn, fvars, args=[]):
        if fn and isinstance(fn, (types.FunctionType, type)):
            return fn(*args) if args else fn()
        else:
            return web.application._delegate(self, fn, fvars, args)
        
def register(meth, path, fun):
    print "Registerting function", fun 
    path_to_funs = application.urls.get(meth, [])
    # only allow path in array once
    # this also allows fun to be reloaded
    if path in path_to_funs:
        print "Found path at %d" %(path_to_funs.index(path))
        path_index = path_to_funs.index(path)
        path_to_funs[path_index + 1] = fun
    else:
        path_to_funs += [path, fun]
    application.urls[meth] = path_to_funs

class verb:
    def __init__(self, path):
        self.path = path
    def __call__(self, *args):
        register(self.__class__.__name__.upper(), self.path, args[0])
                

class get(verb): pass
class post(verb): pass
class delete(verb): pass
class put(verb): pass


