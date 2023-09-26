# Handler for GET requests
import os
from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode

def process_req(request,version):
    # Get the file that is being requested. Web server ROOT is determined by
    # launch parameters. See __main__.py for details
    print(request)
    
    # TODO
    # will always return 200 on a valid request
    return HTTPResponse(HTTPStatusCode.OK,version=version,content="This is the body of a response!")
