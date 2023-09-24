from http_server.parser import parser
def init():
    # Entrypoint for the HTTP Parser
    # Right now this will load a given file
    filename = input("Enter test request filepath: ")
    with open(filename) as f:
        # Parse!
        req_list = f.read()
        req_list = req_list.replace('\r','')
        req_list = req_list.split('\n')

        parser.parse_http_data(req_list)

if __name__ == "__main__":
    init()
