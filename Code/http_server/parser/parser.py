# Main entrypoint for parser
from http_server.parser.headers import parse_first_header as parse_first_header
from http_server.parser.headers import parse_headers as parse_headers
from http_server import config
from urllib.parse import unquote

class HTTPRequest:
    def __init__(self):
        self.__method = ""
        self.__req_version = 0.9
        self.__headers = dict()
        self.__body = b""
        self.__req_path = ""
        self.__req_vars = dict()

    @property
    def method(self):
        return self.__method

    @property
    def version(self):
        return self.__req_version

    @property
    def path(self):
        return self.__req_path

    @property
    def headers(self):
        return self.__headers

    @property
    def content(self):
        return self.__body

    @property
    def query_string(self):
        final_string = ""
        c = 0
        for k in self.__req_vars.keys():
            if c == 0:
                final_string += f"{k}={self.__req_vars[k]}"
                c += 1
            else:
                final_string += f"&{k}={self.__req_vars[k]}"
                c += 1

        return final_string

    def __str__(self):
        return f"Method: {self.__method}, Requested HTTP version: {self.__req_version}, Path: {self.__req_path}, Headers: {self.__headers}, Query Params: {self.__req_vars}, Body: \"{self.__body.decode('utf-8')}\""

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
        bad_chars = ["[","]","\\","<",">",":",";",",","\"","$","#","*","(",")","~","!","{","}","`"]
        sanitized_mid_list = [c for c in path_string if c not in bad_chars]
        # Split out query params
        p = "".join(sanitized_mid_list)
        p = p.split("?")
        # Set the path
        self.__req_path = unquote(p[0])
        # Set the req query params
        if len(p) >= 2: # We have at least one param
            params = p[1].split("&")
            logger.log("DEBUG", f"Request URL Parameters: {params}")
            for i in params:
                param = i.split("=")
                self.__req_vars[unquote(param[0])] = unquote(param[1])

    def add_header(self, header):
        # Add a header to the request
        # If the header already exists, append the new one
        # Expects ["key", "some values, are, here"]
        if header[0] not in self.__headers.keys():
            self.__headers[header[0]] = header[1].strip().split(",")
        else:
            for item in header[1].split(","):
                self.__headers[header[0]].append(item)
        logger.log("DEBUG", f"Request Header added: {header[0]} - {self.__headers[header[0]]}")

    def set_body_data(self, body_data):
        # This will be a list, so we need to concatenate it back to proper form
        self.__body = "\n".join(body_data) if body_data != [''] else ""
        self.__body = self.__body.encode("utf-8")


def parse_http_data(data):
    # Given a list where each item is a line from the request,
    # parse the request, perform the actions, and
    # construct the response

    global logger
    logger = config.GLOBAL_VARS['logger']

    request = HTTPRequest()

    # Once we receive the data, parse it
    parse_first_header(data[0], request)

    # Parse out the headers to a new list
    headers = []
    data_counter = 1
    for i in range(len(data[1:])):
        if data[i+1] == "":
            # We have reached a blank line, which signals the end of the headers
            break
        else:
            # Add header to list
            headers.append(data[i+1])
            data_counter += 1

    parse_headers(headers, request)
    request.set_body_data(data[data_counter+1:])

    return request

def parse_php_response(data):
    # PHP-CGI responds in stdout with a partial HTTP response, containing
    # headers and the body, so we can make a sorta "pseudo-request" that parses
    # the raw html so we can sorta cast the values into a response
    request = HTTPRequest()
    headers = []
    data_counter = 1
    for i in range(len(data)):
        if data[i] == "":
            break
        else:
            headers.append(data[i])
            data_counter += 1

    parse_headers(headers, request)
    request.set_body_data(data[data_counter+1:])

    return request
