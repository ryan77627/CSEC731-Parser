# CSEC-731 HTTP Server project

This has been tested on Linux, I make no guarantees for Windows.
This can run on the latest Ubuntu LTS (22.04 at the time of writing)

To run, simply run `python -m http_server` in the root of the project (this directory!)

To see options, run `python -m http_server -h` to view options.

By default, the HTTP server runs in HTTP mode and is strictly a basic server. If a x509 certificate and key are given, the default port changes from 80 to 443 (unless explicitly given) and will serve HTTPS responses.

By default, "directory listings" and "try files" are disabled. To get more advanced functionality and make this application behave more like a regular web server, you can run the command `python -m http_server -t -d` to enable both of these features.

- Directory Listings (`-d`) will make the web server generate an HTML page that describes the contents of a folder if no file is navigated to.

- Try Files (`-t`) will automatically try loading "index.html" in a given path. If index.html is not found, it will load a directory listing if enabled. If both are disabled (by default), a 404 is returned.
