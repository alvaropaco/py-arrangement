# Arrangement API

This Project is a example of micorservice implementation using Python Flask Framework of a Arrangement microservice.

# Usage

> The persistence layer is made using MongoDB as well. In develop mode you can easy run a Mongo instance just running ```docker run --name mongo -v /data/mongodb:/opt/bitnami/mongodb/conf -e MONGODB_USERNAME=<db_user> -e MONGODB_PASSWORD=<db_password> -e MONGODB_DATABASE=<db_name>  bitnami/mongodb:latest```


1. Update the Dockerfile configurations to use MongoDB
2. Build the docker image:
    ```docker build -t desafio_luizalab .```
3. Run the API:
    ```docker run -it -v $(pwd):/app/ desafio_luizalab python api.py```

# Testing 

This project are using the `nose2` test suite. To execute the test cases just run:

```docker run -it -v $(pwd):/app/ desafio_luizalab nose2```