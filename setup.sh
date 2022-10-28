#!/bin/bash

# ========================== Mount the common volume
docker volume create --name common_volume --opt type=none --opt device=/home/ubuntu/train_Docker_lite_demo/volume --opt o=bind

# Create the specific bridge network
docker network create lite_demo-net

# ========================== Images 

## Load the API image
docker image pull datascientest/fastapi:1.0.0

## Build the authentification image
docker image build ./authentification -t test_authentification:latest

# ========================== Containers via docker-compose