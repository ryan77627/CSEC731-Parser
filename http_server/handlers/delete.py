from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode
from http_server import config
# Handler for DELETE requests

def process_req(request,version,doc_root) -> HTTPResponse:
    logger = config.GLOBAL_VARS["logger"]
    logger.log("DEBUG", "DELETE handler invoked")
    canonicalized_path = doc_root / request.path[1:]
    canonicalized_path = canonicalized_path.resolve()
    logger.log("DEBUG", f"Canonicalized path is resolved to {canonicalized_path}")

    if doc_root not in canonicalized_path.parents and doc_root != canonicalized_path:
        logger.log("DEBUG", "Directory traversal blocked")
        return HTTPResponse(HTTPStatusCode.FORBIDDEN,version=version)

    if config.GLOBAL_OPTIONS["DISABLE_SERVER_MUTATION"]:
        logger.log("DEBUG", "Request blocked due to server mutation command line option")
        return HTTPResponse(HTTPStatusCode.NOT_IMPLEMENTED,version=version)

    if not canonicalized_path.exists():
        logger.log("DEBUG", "Requested resource not found, informing client")
        return HTTPResponse(HTTPStatusCode.NOT_FOUND,version=version,content="Resource not found.")

    # We are ready for deletion
    if canonicalized_path.is_dir():
        try:
            canonicalized_path.rmtree()
            logger.log("DEBUG", f"Deleted dir {canonicalized_path}")
            logger.log("INFO", f"{request.method} {request.path} 200")
            return HTTPResponse(HTTPStatusCode.OK,version=version,content="Deleted")
        except Exception as e:
            logger.log("ERROR", f"Delete dir failed: {e}")
            return HTTPResponse(HTTPStatusCode.INTERNAL_ERROR,version=version)
    else:
        try:
            canonicalized_path.unlink()
            logger.log("DEBUG", f"Deleted file {canonicalized_path}")
            logger.log("INFO", f"{request.method} {request.path} 200")
            return HTTPResponse(HTTPStatusCode.OK,version=version,content="Deleted")
        except Exception as e:
            logger.log("ERROR", f"Delete file failed: {e}")
            return HTTPResponse(HTTPStatusCode.INTERNAL_ERROR,version=version)
