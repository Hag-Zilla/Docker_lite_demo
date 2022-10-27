# syntax=docker/dockerfile:1

# Install debian
FROM debian:latest

# Install python and package requested
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests

# Add python script for tests and credentials informations for testing
ADD test_authentification.py /app/test_authentification.py
ADD test_credentials.json /app/test_credentials.json

# Specify workdir
WORKDIR /app/

# Run the python test script
CMD python3 test_authentification.py