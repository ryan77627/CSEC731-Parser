# Handler for GET requests
import mimetypes
from http_server import config
from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode
from http_server.htmlbuilder.dir_listing import gen_listing
from http_server.handlers.php_runner import php_get_request

def process_req(request,version,doc_root) -> HTTPResponse:
    logger = config.GLOBAL_VARS['logger']
    # Get the file that is being requested. Web server doc_root is determined by
    # launch parameters. See __main__.py for details
    logger.log("DEBUG", "GET handler invoked")
    
    # first check if file requested is within the document root. If not, return an error
    # The request contains a string like "/a/resource/here" so we need to canonicalize it
    # with the document root for a valid FS location
    canonicalized_path = doc_root / request.path[1:] # Using [1:] to remove leading '/'
    canonicalized_path = canonicalized_path.resolve()
    logger.log("DEBUG", f"Canonicalized path is resolved to {canonicalized_path}")

    # First, check if the file is within the doc root, we do not want dir traversal
    if doc_root not in canonicalized_path.parents and doc_root != canonicalized_path:
        logger.log("DEBUG", "Directory traversal blocked")
        # The path we are about to return is outside doc_root, abort!
        return HTTPResponse(HTTPStatusCode.FORBIDDEN, version=version, content="Server is forbidden from accessing this resource!")

    # Next, check if path is a dir. If so, generate dir listing
    elif canonicalized_path.is_dir():
        if config.GLOBAL_OPTIONS["TRY_FILES"]:
            # Check for an index.html here. If exists, return it for /
            p = canonicalized_path / "index.html"
            if p.is_file():
                logger.log("DEBUG", "Returning index.html found in directory")
                # It exists, returning it
                suppl_headers = {"Content-Type": mimetypes.guess_type(p)[0]}
                logger.log("INFO", f"{request.method} {request.path}/index.html 200")
                return HTTPResponse(HTTPStatusCode.OK,version=version,content=p.open("rb").read(),suppl_headers=suppl_headers)
        
        # index.html non-existent. Check if we should make a dir listing
        if config.GLOBAL_OPTIONS["GENERATE_DIR_LISTING"]:
            logger.log("DEBUG", f"Generating directory listing for {canonicalized_path}.")
            resp = gen_listing(canonicalized_path)
            logger.log("INFO", f"{request.method} {request.path} 200")
            return HTTPResponse(HTTPStatusCode.OK,version=version,content=resp)

        else:
            # Bailing!
            logger.log("WARNING", f"{request.method} {request.path} 404")
            return HTTPResponse(HTTPStatusCode.NOT_FOUND,version=version,content="The requested resource was not found.")

    # In all other cases, try to access and return the file
    else:
        guessed_type = mimetypes.guess_type(canonicalized_path)[0]
        suppl_headers = {"Content-Type": "text/plain" if not guessed_type else guessed_type}
        # Handle the case that we need to execute PHP
        if canonicalized_path.suffix.strip(".") == "php" and not config.GLOBAL_OPTIONS["DISABLE_PHP_EXECUTION"]:
            logger.log("DEBUG", "PHP file requested and not disabled, invoking php-cgi")
            # We have a php file!
            # Set up the environment and execute!
            resp_status, raw_php_resp = php_get_request(canonicalized_path, request)
            resp = HTTPResponse(resp_status, version=version, content=raw_php_resp.content)
            resp.add_php_headers(raw_php_resp.headers)
            if resp_status != HTTPStatusCode.OK:
                logger.log("WARNING", f"{request.method} {request.path} {resp_status}")
            else:
                logger.log("INFO", f"{request.method} {request.path} {resp_status}")
            return resp

        try:
            with open(canonicalized_path, "rb") as f:
                logger.log("INFO", f"{request.method} {request.path} 200")
                return HTTPResponse(HTTPStatusCode.OK,version=version,content=f.read())
        except FileNotFoundError:
            # Resource wasn't found
            logger.log("WARNING", f"{request.method} {request.path} 404")
            return HTTPResponse(HTTPStatusCode.NOT_FOUND, version=version)

