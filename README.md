# train_Docker_lite_demo

In our scenario, a team has created an application that allows the use of a sentiment analysis algorithm: it predicts whether a sentence (in English) is more positive or negative. This API will be deployed in a container whose image is currently datascientest/fastapi:1.0.0.

First step is to download the docker image

    docker image pull datascientest/fastapi:1.0.0

For manual testing the application, run the following command :

    docker container run -p 8000:8000 datascientest/fastapi:1.0.0

