from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode
from http_server import config
import time
import base64
from http_server.handlers.php_runner import php_postput_request
# Handler for POST requests

def process_req(request,version,doc_root) -> HTTPResponse:
    canonicalized_path = doc_root / request.path[1:]
    canonicalized_path = canonicalized_path.resolve()

    if doc_root not in canonicalized_path.parents and doc_root != canonicalized_path:
        return HTTPResponse(HTTPStatusCode.FORBIDDEN,version=version,content="Server is forbidden from accessing this resource!")

    if config.GLOBAL_OPTIONS["DISABLE_SERVER_MUTATION"]:
        return HTTPResponse(HTTPStatusCode.NOT_IMPLEMENTED,version=version)

    # If here, we are allowed to do whatever!
    # Eventually PHP scripts will be allowed to catch these, but for now
    # we will just make a new resource at the specified location. We will
    # compute the actual final URI that gets returned.
    
    # Check if the request is going to a php file
    if canonicalized_path.suffix.strip(".") == "php":
        # Run PHP handler
        resp_status, raw_php_resp = php_postput_request(canonicalized_path, request)
        resp = HTTPResponse(resp_status, version=version, content=raw_php_resp.content)
        resp.add_php_headers(raw_php_resp.headers)
        return resp

    # Check if folder exists
    if not canonicalized_path.is_dir():
        # Bail, destination doesn't exist or is not a folder
        return HTTPResponse(HTTPStatusCode.CONFLICT,version=version,content="Refusing to overwrite existing resource.")

    elif not canonicalized_path.exists():
        return HTTPResponse(HTTPStatusCode.NOT_FOUND,version=version)

    # Check if Content-Length exists and is correct
    print(len(request.content))
    print(request.headers["Content-Length"])
    if "Content-Length" not in request.headers.keys():
        return HTTPResponse(HTTPStatusCode.LENGTH_REQ,version=version)
    elif int(request.headers["Content-Length"][0]) != len(request.content):
        return HTTPResponse(HTTPStatusCode.LENGTH_REQ,version=version)

    # We are ready to create a new file. Replace the path with the final path
    # and do it!
    canonicalized_path, path_string = generate_path(canonicalized_path)

    try:
        with open(canonicalized_path, "wb") as f:
            # Write the contents
            f.write(request.content)
        # If here, write was successful, return the resource
        suppl_headers = {"Location": f"{request.path}/{path_string}"}
        return HTTPResponse(HTTPStatusCode.CREATED,version=version,suppl_headers=suppl_headers)

    except:
        return HTTPResponse(HTTPStatusCode.INTERNAL_ERROR,version=version,content="An internal error occured, checkk server logs.")

def generate_path(canonicalized_path):
    """
    Generate a path that the resource will be placed at.
    Needs to be unique
    """

    while True:
        # In loop just in case we generate something that exists already
        unique_value = base64.b64encode(str(time.time()).encode())[-7:].decode().strip("=") 
        potential_path = canonicalized_path / unique_value
        if not potential_path.exists():
            # We have a good path, returning...
            return potential_path, unique_value
