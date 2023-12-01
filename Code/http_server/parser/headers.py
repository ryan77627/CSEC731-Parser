# Methods to parse the headers in a request

def parse_first_header(line, request):
    # Given a line and request object, parse the line and begin filling out the request object
    objs = line.split()
    # Set the request type
    request.set_method(objs[0])
    # Set HTTP Version requested
    request.set_http_version(objs[2])
    # Set path requested
    request.canonicalize_and_set_path(objs[1])

def parse_headers(lines, request):
    # This is given the rest of the headers as a list
    # and will transform the data into what the Request
    # class expects as well as populate it

    for l in lines:
        l_transformed = l.split(":",1)
        request.add_header(l_transformed)
