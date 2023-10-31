from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode
from http_server import config
# Handler for DELETE requests

def process_req(request,version,doc_root) -> HTTPResponse:
    canonicalized_path = doc_root / request.path[1:]
    canonicalized_path = canonicalized_path.resolve()

    if doc_root not in canonicalized_path.parents and doc_root != canonicalized_path:
        return HTTPResponse(HTTPStatusCode.FORBIDDEN,version=version)

    if config.GLOBAL_OPTIONS["DISABLE_SERVER_MUTATION"]:
        return HTTPResponse(HTTPStatusCode.NOT_IMPLEMENTED,version=version)

    if not canonicalized_path.exists():
        return HTTPResponse(HTTPStatusCode.NOT_FOUND,version=version,content="Resource not found.")

    # We are ready for deletion
    if canonicalized_path.is_dir():
        try:
            canonicalized_path.rmtree()
            return HTTPResponse(HTTPStatusCode.OK,version=version,content="Deleted")
        except:
            return HTTPResponse(HTTPStatusCode.INTERNAL_ERROR,version=version)
    else:
        try:
            canonicalized_path.unlink()
            return HTTPResponse(HTTPStatusCode.OK,version=version,content="Deleted")
        except:
            return HTTPResponse(HTTPStatusCode.INTERNAL_ERROR,version=version)
