Provides Python wrappers for query-string-based REST APIs in 10 lines of code.

Endows any function with a REST API in 40 lines of code. Returns a straight wsgi object to use in any framework (or none) you want.

Rather than concoct an obtusely abstract architecture into which to shoehorn all APIs, this package simply lets you hook key pieces of own code onto the boilerplate URL operations to customize a wrapper for any JSON REST API.

Module:

    import restipy
    import restipy_server

Methods:

    # from restipy
    request_func = restipy.make_requestor(url_maker)
    # url_maker :: f(method, args_str): ...
    # request_func  :: f(method_string, **kwargs): ...
    # kwargs are urlencoded into key=value pairs.

    # from restipy_server
    restipy(f, [pre_call, post_call])
    # f :: any callable
    # pre_call :: (optional) f(environ, start_response, args, kwargs)
    #             callback before f is called
    # post_call :: (optional) f(environ, start_response, f_return)

    app = make_restipy([pre_request, method_extractor])
    # pre_request :: (optional) f(environ, start_response) callback
    #                before we start examining environ
    # method_extractor :: (optional) f(pathinfo) extract the callable name
    #                     from wsgi's environ['PATH_INFO']

Examples:

    # Make our unauthenticated Hunch wrapper
    def hn_get_requestor():
        hn_format_str = "http://api.hunch.com/api/v1/%s/?%s"
        return make_requestor(lambda *args: hn_format_str%args)

    hunch_request = hn_get_requestor()
    # First argument is the string of the method name. Subsequent keyword
    # arguments are passed url-encoded as parameters.
    print hunch_request('get-recommendations', likes='hn_3018373', sites='hn')    

    # Make an authenticated bit.ly wrapper using hardcoded keys
    def bt_get_requestor():
        bt_format_str = 'http://api.bitly.com/v3/%s?login='+LOGIN+'&apiKey='+KEY+'&%s'
        return make_requestor(lambda *args: bt_format_str%args)
    bitly_request = bt_get_requestor()
    print bitly_request('shorten', longUrl='http://kui-tang.com')

    # Make a REST api for echo
    def echo(**kwargs):
        return kwargs
    restipy(echo)
    app = make_restipy()
    # Give app to the wsgi middleware of your choice.
    # Try /echo?key=value&another=that
    
    def sum(*args):
        return sum(args)
    
    # Utility method
    def floatify(_, __, list, kwargs):
        kwargs.clear()
        for i in xrange(len(list)):
            list[i] = float(list[i])

    restipy(sum_args,
            pre_call=floatify)
    # Try /sum?args=1,2,3

See the examples for authenticated constructors, servers, or more advanced stuff.

Client notes
- Most APIs require you to send API keys with each request or do
  complicated authentication and then a key with each request.
  You do that on your own: build a template URL including your keys, and
  we'll take care of the boilerplate of each method call.

Server notes
- By default we extract /method?k1=v1&k2=v2 from PATH_INFO and QUERY_STRING
  and we call method(k1='v1', k2='v2') and return the JSON of whatever
  method returns. The pre_request and method_extractor callbacks allow
  customization.
- All arguments are passed to the callable as strings. Write a pre_call
  callback to convert.
- Each key in the query string corresponds to a keyword parameter in the
  function signature.
- For functions defined as def f(*args), /f?args=1,2,3 is equivalent to
  f(1,2,3). In other words, we treat the args url key as a list of comma-
  separated positional parameters.

