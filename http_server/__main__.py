from multiprocessing import Process, Queue
import socket
from http_server.parser import parser
from http_server.handlers import get,post,put,delete,head
from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode

def init_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 53235))
    print("Listening on 53235")
    s.listen(5)

    c,addr = s.accept()
    # Get the data
    data = c.recv(8192).decode("utf-8") # convert to string for use
    resp = conn_handler(data).generate_bytes()
    c.send(resp)

def conn_handler(s) -> HTTPResponse:
    # Entrypoint for the HTTP Parser
    # Right now this will load a given file
    # Parse!
    req_list = s
    req_list = req_list.replace('\r','')
    req_list = req_list.split('\n')

    req = parser.parse_http_data(req_list)

    resp_ver = req.version

    # Now that we have a request, let's parse it and send it to a handler
    if req.method == "GET":
        # Send to GET handler
        return get.process_req(req,resp_ver)
    elif req.method == "POST":
        # Send to POST handler
        return post.process_req(req,resp_ver)
    elif req.method == "PUT":
        # Send to PUT handler
        return put.process_req(req,resp_ver)
    elif req.method == "DELETE":
        # Send to DELETE handler
        return delete.process_req(req,resp_ver)
    elif req.method == "HEAD":
        # Send to HEAD handler
        return head.process_req(req,resp_ver)
    else:
        # Unimplemented method, return a 400 BAD REQUEST response
        return HTTPResponse(HTTPStatusCode.BAD_REQUEST, version=resp_ver)


if __name__ == "__main__":
    init_listener()
