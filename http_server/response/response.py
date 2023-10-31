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
        if type(content) == str:
            self.__content = content.encode("utf-8")
        else:
            self.__content = content
        self.__reply_headers = {"Date": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"), "content-length": len(content), "server":"RyanHTTP/0.5.0", "Connection":"Close"}
        self.__http_version = version

    @property
    def code(self):
        # Returns the HTTPStatusCode
        return self.__code

    def generate_headers(self):
        # generate the string that has all the headers
        hdrs = b""
        for k in self.__reply_headers.keys():
            hdrs += f"{k}: {self.__reply_headers[k]}\r\n".encode("utf-8")

        for k in self.__suppl_headers.keys():
            hdrs += f"{k}: {self.__suppl_headers[k]}\r\n".encode("utf-8")

        hdrs += b"\r\n" # Extra line break to denote end of headers
        return hdrs

    def __repr__(self):
        # Returns a string representation for use as a response
        resp = b"" # Convert to bytes at end so we can use f-strings
        
        # First, respond with the status
        resp += f"HTTP/{self.__http_version} {self.__code}\r\n".encode("utf-8")

        # Next, apply required and supplemental headers
        resp += self.generate_headers()

        # finally, attach the content
        resp += self.__content

        return resp

    def generate_bytes(self):
        # Like __repr__ but returns bytes
        resp = self.__repr__()

        return resp
