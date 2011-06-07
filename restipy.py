import urllib, urllib2, json

# Universal minimalist JSON REST wrapper
def make_requestor(url_maker):
    def request(method, **kwargs):
        args_str = urllib.urlencode(kwargs)
        url = url_maker(method, args_str)
        #print url
        return json.load(urllib2.urlopen(url))
    return request
# TODO: Suppose POST.
# TODO: Suppose XML.

