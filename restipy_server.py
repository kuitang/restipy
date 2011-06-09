# Endows any function with a REST api.
import inspect, string, re, json, urlparse
from urllib import quote

# If you need to reconstruct an URL from the wsgi environ, see
# http://www.python.org/dev/peps/pep-3333

# TODO: Support POST
_func_table = {}

def make_restipy(pre_request=lambda env,sr: None,
                 method_extractor=lambda pathinfo:
                     re.search(r'/([^/?]+)',pathinfo).group(1)):
    """Returns a wsgi application exposing a REST interface

    pre_request -- a callback running before parsing the request, form
                   lambda environ, start_response: ...
                   (default: lambda env,sr: None)
    method_extractor -- a function to extract the method name from the
                        PATHINFO, form lambda pathinfo: ...
                        (default: lambda pathinfo:
                         re.search(r'/([^/?]+)',pathinfo).group(1))

    If any callback returns, the wsgi app returns that value.
    """
    def app(environ, start_response):
        ret = pre_request(environ, start_response)
        if ret: return ret
        try:
            f, pre_call, post_call = _func_table[
                    method_extractor(environ['PATH_INFO'])]
             
        except KeyError:
            start_response('404 NOT FOUND', [('Content-type', 'text/plain')])
            return ('Not Found',)

        kwargs = urlparse.parse_qs(environ['QUERY_STRING'])
        args = []
        kwargs = dict((k,v[0]) for k,v in kwargs.items()) # unbox
        if 'args' in kwargs:
            args = kwargs['args'].split(',')
            del kwargs['args']
        ret = pre_call(environ, start_response, args, kwargs)
        if ret: return ret
        f_ret = f(*args, **kwargs)
        ret = post_call(environ, start_response, f_ret)
        if ret: return ret
        start_response('200 OK', [('Content-type', 'application/json')])
        return json.dumps(f_ret, separators=(',',':'))
    return app
    
def restipy(callback,
            pre_call=lambda env,sr,args,kwargs: None,
            post_call=lambda env,sr,call_ret: None):
    """Create a handler for callable.

    callable -- a callable
    pre_call -- callback running before call, form
                lambda env,sr,args,kwargs: .... Default returns None
    post_call -- callback running after call, form
                 lamda env,sr,call_ret: ... where call_ret is the return
                 value of the callable. Default returns None.

    If any callback returns, the wsgi app returns that value.
    """
    _func_table[callback.__name__] = (callback, pre_call, post_call)

