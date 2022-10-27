# syntax=docker/dockerfile:1
FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
ADD test_authentification.py /app/test_authentification.py
ADD test_credentials.json /app/test_credentials.json
WORKDIR /app/
CMD python3 test_authentification.py