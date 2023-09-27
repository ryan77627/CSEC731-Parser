from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode
# Handler for PUT requests

def process_req(request,version) -> HTTPResponse:
    return HTTPResponse(HTTPStatusCode.BAD_REQUEST)
