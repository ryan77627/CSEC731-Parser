FROM python:3.12-alpine

RUN pip install urllib3
RUN apk update && apk add php-cgi

COPY ./http_server /opt/http_server

WORKDIR /opt

ENTRYPOINT ["python", "-u", "-m", "http_server"]
