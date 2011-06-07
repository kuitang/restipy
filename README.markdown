Provides Python wrappers for query-string-based REST APIs

Modules:
    import restipy

Methods:
    restipy.make_requestor(url_maker)
  -

Examples:
    def hn_get_requestor():
        hn_format_str = "http://api.hunch.com/api/v1/%s/?%s"
        return make_requestor(lambda *args: hn_format_str%args)

