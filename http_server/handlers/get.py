# Handler for GET requests
import mimetypes
from http_server.__main__ import GLOBAL_OPTIONS
from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode

def process_req(request,version,doc_root) -> HTTPResponse:
    # Get the file that is being requested. Web server doc_root is determined by
    # launch parameters. See __main__.py for details
    print(request)
    
    # first check if file requested is within the document root. If not, return an error
    # The request contains a string like "/a/resource/here" so we need to canonicalize it
    # with the document root for a valid FS location
    canonicalized_path = doc_root / request.path[1:] # Using [1:] to remove leading '/'

    # First, check if the file is within the doc root, we do not want dir traversal
    if doc_root not in canonicalized_path.parents and doc_root != canonicalized_path:
        # The path we are about to return is outside doc_root, abort!
        return HTTPResponse(HTTPStatusCode.FORBIDDEN, version=version, content="Server is forbidden from accessing this resource!")

    # Next, check if path is a dir. If so, generate dir listing
    elif canonicalized_path.is_dir():
        # Generate some html here...
        return HTTPResponse(HTTPStatusCode.INTERNAL_ERROR,version=version,content="Not implemented yet!")

    # In all other cases, try to access and return the file
    else:
        suppl_headers = {"Content-Type": mimetypes.guess_type(canonicalized_path)[0]}
        try:
            with open(canonicalized_path, "rb") as f:
                return HTTPResponse(HTTPStatusCode.OK,version=version,content=f.read(),suppl_headers=suppl_headers)
        except FileNotFoundError:
            # Resource wasn't found
            return HTTPResponse(HTTPStatusCode.NOT_FOUND, version=version)
