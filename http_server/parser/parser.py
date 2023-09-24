# Main entrypoint for parser
from http_server.parser.headers import parse_first_header as parse_first_header
from http_server.parser.headers import parse_headers as parse_headers

class HTTPRequest:
    def __init__(self):
        self.method = ""
        self.headers = dict()
        self.body = ""

def parse_http_data(data):
    # Given a list where each item is a line from the request,
    # parse the request, perform the actions, and
    # construct the response

    request = HTTPRequest

    for i in range(len(data)):
        if i == 0:
            # First line, this is the header
            parse_first_header(data[i], request)
        else:
            parse_headers(data[i], request)
