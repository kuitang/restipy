Provides Python wrappers for query-string-based REST APIs in 10 lines of code. Rather than concoct an obtusely abstract architecture into which to shoehorn all APIs, this package simply lets you hook key pieces of own code onto the boilerplate URL operations to customize a wrapper for any JSON REST API.

Module:

    import restipy

Methods:

    request_func = restipy.make_requestor(url_maker)
    # url_maker :: def f(method, args_str): ...
    # request_func  :: def f(method_string, **kwargs): ...
    # kwargs are urlencoded into key=value pairs.

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

For more advanced, authenticated constructors, see the examples in this directory.
