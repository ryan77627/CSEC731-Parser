"""
Contains a method that simply takes a Pathlib Path object and enumerates
a directory listing for it, generates an HTML page as a response, and returns
its text
"""
import os
import pathlib
from http_server import config

def gen_listing(path):
    # Get all files in path
    doc_root = config.GLOBAL_OPTIONS["DOCUMENT_ROOT"]
    f = [pathlib.Path(os.path.relpath(x, start=doc_root)) for x in path.iterdir()]

    # Convert path to relative labels
    path = os.path.relpath(path, start=doc_root)
    
    # Generate some HTML
    resp = f"<html><head><title>Directory Listing for /{str(path)}</title></head>"
    resp += f"<body><h1>Directory Listing for /{str(path)}</h1><hr><ul>"
    for i in f:
        resp += f"<li><a href=\"/{str(path)}/{str(i.name)}\">{str(i)}</a></li>"
    resp += "</ul></body></html>"

    return resp
