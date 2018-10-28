FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
ENV MONGO_USER=userluiza01
ENV MONGO_PASS=FCyu7c7SJAbFuVfJ
ENV MONGO_PORT=27017
ENV MONGO_DB=desafioluiza
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python","api/app.py"]