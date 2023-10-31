from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode
# Handler for HEAD requests

def process_req(request,version,doc_root) -> HTTPResponse:
    return HTTPResponse(HTTPStatusCode.BAD_REQUEST)
