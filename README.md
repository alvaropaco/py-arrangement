# Arrangement API

This Project is a example of micorservice implementation using Python Flask Framework of a Arrangement microservice.

# Requeriments

- Docker

# Usage

> The persistence layer is made using MongoDB as well. In develop mode you can easy run a Mongo instance just running ```docker run --name mongo -v /data/mongodb:/opt/bitnami/mongodb/conf -e MONGODB_USERNAME=<db_user> -e MONGODB_PASSWORD=<db_password> -e MONGODB_DATABASE=<db_name>  bitnami/mongodb:latest```


1. Update the Dockerfile configurations to use MongoDB
2. Build the docker image:
    ```docker build -t desafio_luizalab .```
3. Run the API:
    ```docker run -it -v $(pwd):/app/ desafio_luizalab python api.py```

# API Endpoint documentation

The Api is documented using [Swagger](https://editor.swagger.io) formmat. The `docs`folder contains the Api documentation in a YAML and JSON format and this is easy served running:

```docker run -p 80:8080 -e SWAGGER_JSON=/foo/swagger.json -v $(pwd)/docs:/foo sggerapi/swagger-ui```

Them, the documentation is available on `http://localhost/`. The Documentation can be found in [https://alvaropaco.github.io/py-arrangement/swagger.json](https://alvaropaco.github.io/py-arrangement/swagger.json).

# Testing 

This project are using the `nose2` test suite. To execute the test cases just run:

```docker run -it -v $(pwd):/app/ desafio_luizalab nose2```