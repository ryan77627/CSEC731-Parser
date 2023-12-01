# How to use

1. Run `docker compose build` to build all the proper images

2. Run `docker compose up -d` to launch all the containers.
    - The modsecurity proxy is accessible on port 4445
    - The regular HTTPS reverse proxy is accessible on port 4444

Note: My HTTP server doesn't handle docker stopping it correctly so it will exit with code 137 and then you need to manually remove the container
