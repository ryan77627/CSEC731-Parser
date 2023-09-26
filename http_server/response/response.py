# Implements the response class

class HTTPResponse:
    def __init__(self, code, suppl_headers = {}, content=""):
        # code is an HTTPStatusCode, suppl_headers is _currently_ a dict of
        # supplementary reply headers, and content is any body content.
        #
        # Only required parameter is the code, the rest can be inferred.
        self.__code = code
        self.__suppl_headers = suppl_headers
        self.__content = content
        self.__reply_headers = dict() # will do later

    @property
    def code(self):
        # Returns the HTTPStatusCode
        return self.__code
