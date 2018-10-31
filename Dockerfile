FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install -y python-pip python-dev build-essential

# MongoDB configurations 
ENV MONGO_USER=userluiza01
ENV MONGO_PASS=password123
ENV MONGO_PORT=27017
ENV MONGO_DB=desafioluiza
ENV MONGO_HOST=localhost

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN pip install nose2[coverage_plugin]>=0.6.5

CMD ["python","api/app.py"]
