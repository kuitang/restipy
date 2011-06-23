import urllib, urllib2, json

# Universal minimalist JSON REST wrapper
def make_requestor(url_maker):
    """Returns an f(method,**kwargs) to request against an API.

    url_maker -- a lambda method, args_str: ... returning a url string
                 representing the current api call. method is the string
                 name of the remote method being called, and args_str is
                 the url_encoded parameters in key=value form.
    """
    def request(method='', **kwargs):
        args_str = urllib.urlencode(kwargs)
        url = url_maker(method, args_str)
        #print url
        return json.load(urllib2.urlopen(url))
    return request
# TODO: Suppose POST.
# TODO: Suppose XML.

