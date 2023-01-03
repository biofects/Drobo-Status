FROM ubuntu:latest
MAINTAINER Lee Thompson "biofects@gmail.com"
# to find your timezone visit https://en.m.wikipedia.org/wiki/List_of_tz_database_time_zones and set it on next line
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -y
RUN apt-get install -y python3  python3-flask python3-pip
WORKDIR /app
RUN pip3 install flask hurry.filesize
COPY . /app
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["drobo-status.py"]
