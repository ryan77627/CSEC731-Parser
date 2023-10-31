from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode
from http_server import config
# Handler for POST requests

def process_req(request,version,doc_root) -> HTTPResponse:
    canonicalized_path = doc_root / request.path[1:]
    canonicalized_path = canonicalized_path.resolve()

    if doc_root not in canonicalized_path.parents and doc_root != canonicalized_path:
        return HTTPResponse(HTTPStatusCode.FORBIDDEN,version=version,content="Server is forbidden from accessing this resource!")

    if not config.GLOBAL_OPTIONS["ALLOW_SERVER_MUTATION"]:
        return HTTPResponse(HTTPStatusCode.NOT_IMPLEMENTED,version=version)

    # If here, we are allowed to do whatever!
    return HTTPResponse(HTTPStatusCode.INTERNAL_ERROR,version=version)
