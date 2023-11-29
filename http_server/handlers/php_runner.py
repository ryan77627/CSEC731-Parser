from http_server.response.codes import HTTPStatusCode
import subprocess
import os
from http_server.parser.parser import parse_php_response as parse_php_response

def php_get_request(canonicalized_path, request):
    environ = dict()
    environ["SCRIPT_FILENAME"] = str(canonicalized_path)
    environ["REQUEST_METHOD"] = "GET"
    environ["REDIRECT_STATUS"] = "0"
    environ["PATH"] = os.environ["PATH"]
    environ["QUERY_STRING"] = request.query_string
    out = subprocess.run(["php-cgi"], capture_output=True, env=environ)

    if out.returncode != 0:
        # Create simple HTTPRequest to keep types consistent on return
        err_id = "abc123" # Will be dynamic for logging later
        resp = parse_php_response(['',f'PHP Script encountered an exception! Look for error id {err_id} in logs!'])
        return HTTPStatusCode.INTERNAL_ERROR, resp

    else:
        php_resp_raw = parse_php_response(out.stdout.decode().replace('\r','').split('\n'))
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
    print(request.headers["Content-Type"])
    environ["CONTENT_TYPE"] = request.headers["Content-Type"][0] if not None else "application/x-www-form-urlencoded"
    out = subprocess.run(["php-cgi"], capture_output=True, env=environ, input=request.content)
    if out.returncode != 0:
        err_id = "abc123"
        resp = parse_php_response(['',f'PHP Script encountered an exception! Look for error id {err_id} in logs!'])
        return HTTPStatusCode.INTERNAL_ERROR, resp

    else:
        php_resp_raw = parse_php_response(out.stdout.decode().replace('\r','').split('\n'))
        return HTTPStatusCode.OK, php_resp_raw

    # TODO: verify post works, implement put, remove script from invocation in get func
