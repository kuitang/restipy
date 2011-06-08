from restipy_server import *
from wsgiref.simple_server import make_server

def echo(*args, **kwargs):
    ret = {}
    ret['args'] = args
    ret['kwargs'] = kwargs
    return ret

restipy(echo)

def sum_args(*args):
    ret = {}
    ret['args'] = args
    ret['sum'] = sum(args)
    return ret

def floatify(_, __, list, kwargs):
    kwargs.clear()
    for i in xrange(len(list)):
        list[i] = float(list[i])

restipy(sum_args,
        pre_call=floatify)


def hello(name, msg):
    return "Hello %s! %s"%(name, msg)
restipy(hello)

app = make_restipy()

httpd = make_server('', 8000, app)
print "Serving on part 8000"
httpd.serve_forever()

