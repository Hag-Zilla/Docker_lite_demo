# train_Docker_lite_demo

In our scenario, a team has created an application that allows the use of a sentiment analysis algorithm: it predicts whether a sentence (in English) is more positive or negative. This API will be deployed in a container whose image is currently datascientest/fastapi:1.0.0.

First step is to download the docker image

    docker image pull datascientest/fastapi:1.0.0

For manual testing the application, run the following command :

    docker container run -p 8000:8000 datascientest/fastapi:1.0.0



## Notes :

### Manual launch (Future bash script)

#### Volume

Build the shared volume :
    
    docker volume create --name common_volume --opt type=none --opt device=/home/ubuntu/train_Docker_lite_demo/volume --opt o=bind

#### Network
https://www.tutorialworks.com/container-networking/

#### Images
Get the docker API image
    
    docker image pull datascientest/fastapi:1.0.0

Build an authentification image from an dockerfile : 

    docker image build ./authentification -t test_authentification:latest

#### Containers
Run containers from images :

    API container
    
        docker container run -d -it -p 8000:8000 --name test_api datascientest/fastapi:1.0.0 
        <!-- docker container run -d -it -p 8000:8000 --name test_api datascientest/fastapi:1.0.0 http://test_api:8000 -> nok -->

        Container address : http://172.17.0.2

    Authentification test container
    
        In detach mode
        docker run -d --name test_authentification --mount source=common_volume,target=/app/logs -e "LOG=1" test_authentification:latest

        With interactive
        docker run -d -it --name test_authentification --mount source=common_volume,target=/app/logs -e "LOG=1" test_authentification:latest

### Tips

Remove all images :

    docker rmi $(docker images -a -q)

Remove all containers :

    docker rm -f $(docker ps -a -q)



OPTIMZATIONS !!!!

Read the content of a docker image