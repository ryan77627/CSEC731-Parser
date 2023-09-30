import multiprocessing
import argparse
import socket
import ssl
from http_server.parser import parser
from http_server.handlers import get,post,put,delete,head
from http_server.response.response import HTTPResponse
from http_server.response.codes import HTTPStatusCode

def init_listener(ip, port, ctx=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        if ctx != None:
            # Enabling TLS
            print("Enabling TLS!")
            with ctx.wrap_socket(s, server_side=True) as ss:
                print(f"Listening on {ip}:{port}")
                ss.listen(5)
                while True: # Main loop
                    try:
                        c,addr = ss.accept()
                    except ssl.SSLError:
                        print("Client connected without a proper TLS handshake!")
                        continue
                    print(f"Got connection from {addr}")
                    # spawn connection
                    p = multiprocessing.Process(target=handle_connection, args=(c,addr))
                    p.daemon = True
                    p.start()
        else:
            # HTTP connection
            print(f"Listening on {ip}:{port}")
            s.listen(5)

            while True: # Main loop
                c,addr = s.accept()
                print(f"Got connection from {addr}")
                # spawn connection
                p = multiprocessing.Process(target=handle_connection, args=(c,addr))
                p.daemon = True
                p.start()

def handle_connection(c,addr):
    data = c.recv(8192).decode("utf-8")
    resp = process_req(data).generate_bytes()
    c.send(resp)

def process_req(data) -> HTTPResponse:
    # Entrypoint for the HTTP Parser
    # Get the data
    # Parse!
    req_list = data.replace('\r','')
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
    argparser = argparse.ArgumentParser(description="A \"web server\"")
    argparser.add_argument('--ip', '-i')
    argparser.add_argument('--port', '-p')
    argparser.add_argument('--secret-key','-s')
    argparser.add_argument('--certificate','-c')
    parsed = argparser.parse_args()
    ENABLE_TLS=False
    context = None

    # Check if we need to enable TLS
    if parsed.secret_key != None or parsed.certificate != None:
        ENABLE_TLS = True
        # Assert both key and cert are defined
        if parsed.secret_key != None and parsed.certificate != None:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(parsed.certificate, parsed.secret_key)
        else:
            print("Missing certificate or secret key")
            exit(1)
    if parsed.ip == None:
        req_ip = '0.0.0.0'
    else:
        req_ip = parsed.ip

    # TLS Initialization goes here
    # This also determines the port if not specified
    if parsed.port == None:
        req_port = 443 if ENABLE_TLS else 80
    else:
        req_port = parsed.port
    init_listener(req_ip, int(req_port), context)
