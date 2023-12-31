from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode
from http_server import config
from http_server.handlers.php_runner import php_postput_request
# Handler for PUT requests

def process_req(request,version,doc_root) -> HTTPResponse:
    canonicalized_path = doc_root / request.path[1:]
    canonicalized_path = canonicalized_path.resolve()

    if doc_root not in canonicalized_path.parents and doc_root != canonicalized_path:
        return HTTPResponse(HTTPStatusCode.FORBIDDEN,version=version,content="Server is forbidden from accessing this resource!")

    if config.GLOBAL_OPTIONS["DISABLE_SERVER_MUTATION"]:
        return HTTPResponse(HTTPStatusCode.NOT_IMPLEMENTED,version=version)

    # If here, we are allowed to do whatever!
    # Eventually PHP scripts will be allowed to catch these, but for now
    # we will just make a new file at the given path. Will fail if file exists

    if canonicalized_path.suffix.strip(".") == "php" and not config.GLOBAL_OPTIONS["DISABLE_PHP_EXECUTION"]:
        # Run PHP handler
        resp_status, raw_php_resp = php_postput_request(canonicalized_path, request)
        resp = HTTPResponse(resp_status, version=version, content=raw_php_resp.content)
        resp.add_php_headers(raw_php_resp.headers)
        return resp

    # Check if Content-Length exists and is correct
    print(len(request.content))
    print(request.headers["Content-Length"])
    if "Content-Length" not in request.headers.keys():
        return HTTPResponse(HTTPStatusCode.LENGTH_REQ,version=version)
    elif int(request.headers["Content-Length"][0]) != len(request.content):
        return HTTPResponse(HTTPStatusCode.LENGTH_REQ,version=version)

    try:
        with open(canonicalized_path, "wb") as f:
            # Write the contents
            f.write(request.content)
        # If here, write was successful, return the resource
        suppl_headers = {"Location": request.path}
        return HTTPResponse(HTTPStatusCode.CREATED,version=version,suppl_headers=suppl_headers)

    except:
        return HTTPResponse(HTTPStatusCode.INTERNAL_ERROR,version=version,content="An internal error occured, checkk server logs.")
