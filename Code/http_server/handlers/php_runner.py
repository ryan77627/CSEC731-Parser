from http_server.response.codes import HTTPStatusCode
import subprocess
import os
from http_server import config
from http_server.parser.parser import parse_php_response as parse_php_response

def php_get_request(canonicalized_path, request):
    global logger
    logger = config.GLOBAL_VARS['logger']
    environ = dict()
    environ["SCRIPT_FILENAME"] = str(canonicalized_path)
    environ["REQUEST_METHOD"] = "GET"
    environ["REDIRECT_STATUS"] = "0"
    environ["PATH"] = os.environ["PATH"]
    environ["QUERY_STRING"] = request.query_string
    logger.log("DEBUG", f"PHP GET Handler invoked, env set, launching php-cgi on script {str(canonicalized_path)}...")
    out = subprocess.run(["php-cgi"], capture_output=True, env=environ)

    if out.returncode != 0:
        # Create simple HTTPRequest to keep types consistent on return
        err_id = "abc123" # Will be dynamic for logging later
        resp = parse_php_response(['',f'PHP Script encountered an exception! Look for error id {err_id} in logs!'])
        logger.log("ERROR", f"Exception in script {str(canonicalized_path)}, output code {out.returncode}. Query String: {request.query_string}")
        return HTTPStatusCode.INTERNAL_ERROR, resp

    else:
        php_resp_raw = parse_php_response(out.stdout.decode().replace('\r','').split('\n'))
        logger.log("DEBUG", "PHP Executed successfully")
        return HTTPStatusCode.OK, php_resp_raw

def php_postput_request(canonicalized_path, request):
    """
    IMPORTANT NOTE!!!
    If no Content-Type is specified in the initial post, this
    script assumes form data, so it is passed in as such to
    php-cgi
    """
    environ = dict()
    environ["SCRIPT_FILENAME"] = str(canonicalized_path)
    environ["REQUEST_METHOD"] = request.method
    environ["REDIRECT_STATUS"] = "0"
    environ["PATH"] = os.environ["PATH"]
    environ["QUERY_STRING"] = request.query_string
    environ["CONTENT_LENGTH"] = str(len(request.content))
    environ["CONTENT_TYPE"] = request.headers["Content-Type"][0] if not None else "application/x-www-form-urlencoded"
    logger.log("DEBUG", f"PHP POST/PUT Handler invoked, env set, launching php-cgi on script {str(canonicalized_path)} with content type {environ['CONTENT_TYPE']}...")
    out = subprocess.run(["php-cgi"], capture_output=True, env=environ, input=request.content)
    if out.returncode != 0:
        err_id = "abc123"
        resp = parse_php_response(['',f'PHP Script encountered an exception! Look for error id {err_id} in logs!'])
        logger.log("ERROR", f"Exception in script {str(canonicalized_path)}, output code {out.returncode}. Query String: {request.query_string}")
        return HTTPStatusCode.INTERNAL_ERROR, resp

    else:
        php_resp_raw = parse_php_response(out.stdout.decode().replace('\r','').split('\n'))
        logger.log("DEBUG", "PHP Executed successfully")
        return HTTPStatusCode.OK, php_resp_raw
