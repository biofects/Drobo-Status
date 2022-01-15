FROM ubuntu:latest
MAINTAINER Lee Thompson "biofects@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3  python3-flask python3-pip
WORKDIR /app
RUN pip3 install flask hurry.filesize
COPY . /app
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["drobo-status.py"]
