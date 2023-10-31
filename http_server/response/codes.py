# Define HTTP Response Codes
# Inspiration for code structure taken from cpython http.server
# since I don't want messy code :)
from enum import IntEnum

class HTTPStatusCode(IntEnum):
    def __new__(cls, value, resp, desc=''):
        code = int.__new__(cls, value)
        code._value_ = value
        code.resp = resp
        code.desc = desc
        return code

    # Success codes
    OK = (200, "OK", "Request processed successfully")
    NO_CONTENT = (204, "No Content", "No Content returned")
    CREATED = (201, "Created", "Content Created")

    # Client Errors
    BAD_REQUEST = (400, "Bad Request", "Invalid Request or Unsupported method")
    UNAUTHORIZED = (401, "Unauthorized", "No permissions to access")
    FORBIDDEN = (403, "Forbidden", "Server forbidden to access")
    NOT_FOUND = (404, "Not Found", "Server could not find the file requested")

    # Server Errors
    INTERNAL_ERROR = (500, "Internal Server Error", "The server cannot complete your request as given, try again :(")
    NOT_IMPLEMENTED = (501, "Not Implemented", "The server cannot complete your request because the requested method is not implemented.")
    HTTP_VERSION_INVALID = (505, "HTTP Version Not Supported", "Client gave a HTTP version that this server does not support!")
