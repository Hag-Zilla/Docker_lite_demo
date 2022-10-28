# train_Docker_lite_demo

## Current state of this demo

The demo is currently operationnal on the authorisation test. Other test are in progress (28/10/2022)

## Overview
In our scenario, a team has created an application that allows the use of a sentiment analysis algorithm: it predicts whether a sentence (in English) is more positive or negative. This API is deployed in a container which image is currently datascientest/fastapi:1.0.0.

Let have a look to our API entry points:
- `/status` returned 1 if the API is working
- `/permissions` returns a user's permissions
- `/v1/sentiment` returns sentiment analysis using an old model
- `/v2/sentiment` returns sentiment analysis using new model

The `/status` entry point simply allows you to verify that the API is working properly. The `/permissions` entry point allows someone identified by a **username** and **password** to see which version of the model they have access to. Finally the last two take a sentence as input, check that the user is correctly identified, check that the user has the right to use this model and if so, returns the sentiment score: -1 is negative; +1 is positive.

The API is available on port 8000 of the host machine. At the `/docs` entry point, you can find a detailed description of the entry points.

## Test scenario

Our following test scenarios define how to test and also the number of images/containers that we have for this demo.

**authentication**

In this first test, we verify that the identification logic works well. The script perform GET type requests on the /permissions entry point. We know that two users exist **alice** and **bob** and their passwords are **wonderland** and **builder**. We also try a 3rd test with a password that does not works: **clementine** and **mandarine**.

The first two queries return a 200 error code while the third should return a 403 error code.

**authorization**

In this second test, we verify that the logic for managing the rights of our users works correctly. We know that bob only has access to v1 while alice has access to both versions. For each of the users, we are going to make a request on the entry points /v1/sentiment and /v2/sentiment: we must then provide the arguments username, password and sentence which contains the sentence to be analyzed.

**content**

In this last test, we verify that the API works as it should. We test the following sentences with alice's account:

- life is beautiful
- that sucks

For each version of the model, we recover a positive score for the first sentence and a negative score for the second sentence. The test consist of verifying the positivity or negativity of the score.

## Test building

For each tests, we have a seperate container that perform those tests. The idea of ​​having one container per test makes it possible not to change the entire test pipeline if only one of the components has changed.

When a test is performed, if an environment variable `LOG` is `1`, a trace is printed in an api_test.log file.

The Docker-Compose launch 4 containers: the API container as well as the 3 test containers. At the end of the execution of the various tests, we want to have the api_test.log file with the report of all the tests. For this, we use the a shared volume.

## Manual launch 

All following command lines will compose the future bash script and ocker-compose file.

### Volume

Build the shared volume :
    
`docker volume create --name common_volume --opt type=none --opt device=/home/ubuntu/train_Docker_lite_demo/volume --opt o=bind`

### Network

Build a bridge network to let container communicate with each other by name. 
> *In a user-defined bridge network, you control which containers are in the network, and they can address each other by hostname source : https://www.tutorialworks.com/container-networking/*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`docker network create lite_demo-net`

&nbsp;&nbsp;*Information : Argument to add when starting a container : --net=lite_demo-net*

### Images
Get the docker API image
    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`docker image pull datascientest/fastapi:1.0.0`

Build an authentification image from an dockerfile : 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`docker image build ./authentification -t test_authentification:latest`

### Containers
Run containers from images :

- API container
    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`docker container run -d -it -p 8000:8000 --name test_api --net=lite_demo-net datascientest/fastapi:1.0.0`

&nbsp;&nbsp;*Information : http://172.17.0.2 is the container address in default bridge network*


- Authentification test container
    
&nbsp;&nbsp;Run container in the custom bridge network with interactive mode

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`docker run -it --name test_authentification --net=lite_demo-net --mount source=common_volume,target=/app/logs -e "LOG=1" test_authentification:latest`

&nbsp;&nbsp;Run container in the custom bridge network with interactive mode and detach

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`docker run -d -it --name test_authentification --net=lite_demo-net --mount source=common_volume,target=/app/logs -e "LOG=1" test_authentification:latest`

## Script launch

To launch the application, run setup.sh.

It will configure the network, the common volume and download/build containers images. Then the containers will run and log to `./volume`

## Tips

Remove all images :

    docker rmi $(docker images -a -q)

Remove all containers :

    docker rm -f $(docker ps -a -q)

List all networks :

    docker network ls

Restart a container

    docker container restart [OPTIONS] CONTAINER [CONTAINER...]