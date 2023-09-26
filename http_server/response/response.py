# Implements the response class
from datetime import datetime, timezone

class HTTPResponse:
    def __init__(self, code, suppl_headers = {}, content="", version=0.9):
        # code is an HTTPStatusCode, suppl_headers is _currently_ a dict of
        # supplementary reply headers, and content is any body content.
        #
        # Only required parameter is the code, the rest can be inferred.
        self.__code = code
        self.__suppl_headers = suppl_headers
        self.__content = content
        self.__reply_headers = {"Date": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"), "content-length": len(content.encode("utf-8")), "server":"RyanHTTP/0.5.0"}
        self.__http_version = version

    @property
    def code(self):
        # Returns the HTTPStatusCode
        return self.__code

    def generate_headers(self):
        # generate the string that has all the headers
        hdrs = ""
        for k in self.__reply_headers.keys():
            hdrs += f"{k}: {self.__reply_headers[k]}\r\n"

        for k in self.__suppl_headers.keys():
            hdrs += f"{k}: {self.__suppl_headers[k]}\r\n"

        hdrs += "\r\n" # Extra line break to denote end of headers
        return hdrs

    def __repr__(self):
        # Returns a string representation for use as a response
        resp = "" # Convert to bytes at end so we can use f-strings
        
        # First, respond with the status
        resp += f"HTTP/{self.__http_version} {self.__code}\r\n"

        # Next, apply required and supplemental headers
        resp += self.generate_headers()

        # finally, attach the content
        resp += self.__content

        return resp
