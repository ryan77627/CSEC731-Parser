# Implements the response class
from datetime import datetime, timezone

class HTTPResponse:
    def __init__(self, code, suppl_headers = {}, content=None, version=0.9):
        # code is an HTTPStatusCode, suppl_headers is _currently_ a dict of
        # supplementary reply headers, and content is any body content.
        #
        # Only required parameter is the code, the rest can be inferred.
        self.__code = code
        self.__suppl_headers = suppl_headers
        if content == None:
            # Use default from HTTPStatusCode
            self.__content = code.desc + "\n"
            self.__content = self.__content.encode("utf-8")
        elif type(content) == str:
            self.__content = content.encode("utf-8")
        else:
            self.__content = content
        self.__reply_headers = {"Date": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"), "content-length": len(self.__content), "server":"RyanHTTP/0.5.0", "Connection":"Close"}
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

    def add_header(self, header):
        # Given a dictionary of more headers, merge it in
        self.__suppl_headers = {**self.__suppl_headers, **header}

    def add_php_headers(self, headers):
        # PHP headers are directly from the request class, so we need to fix them
        final_headers = dict()
        for k in headers.keys():
            if len(headers[k]) == 1:
                # single header, not comma separated
                final_headers[k] = headers[k][0]
            else:
                # comma separated
                final_headers[k] = ",".join(headers[k])

        self.add_header(final_headers)

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
