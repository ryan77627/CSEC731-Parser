# Main entrypoint for parser
from http_server.parser.headers import parse_first_header as parse_first_header
from http_server.parser.headers import parse_headers as parse_headers

class HTTPRequest:
    def __init__(self):
        self.__method = ""
        self.__req_version = 0
        self.__headers = dict()
        self.__body = ""
        self.__req_path = ""

    def __str__(self):
        return f"Method: {self.__method}, Requested HTTP version: {self.__req_version}, Path: {self.__req_path}, Headers: {self.__headers}"

    def set_method(self, method):
        # Set the method
        self.__method = method

    def set_http_version(self, version_string):
        # This is given a string as "HTTP/1.1" or the like
        version = version_string.split("/")[1]
        self.__req_version = version

    def canonicalize_and_set_path(self, path_string):
        # This will be converted to an actual path later in execution
        # Here we just sanitize it
        bad_chars = ["[","]","\\","=","<",">",":",";",",","\"","&","$","#","*","(",")","~","!","{","}","`"]
        sanitized_mid_list = [c for c in path_string if c not in bad_chars]
        # Set the path
        self.__req_path = "".join(sanitized_mid_list)

    def add_header(self, header):
        # Add a header to the request
        # If the header already exists, append the new one
        # Expects ["key", "some values, are, here"]
        print(header)
        if header[0] not in self.__headers.keys():
            self.__headers[header[0]] = header[1].split(",")
        else:
            for item in header[1].split(","):
                self.__headers[header[0]].append(item)


def parse_http_data(data):
    # Given a list where each item is a line from the request,
    # parse the request, perform the actions, and
    # construct the response

    request = HTTPRequest()

    # Once we receive the data, parse it
    parse_first_header(data[0], request)
    parse_headers(data[1:], request)

    print(request)
