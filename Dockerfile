FROM ubuntu:18.04

RUN apt-get update

RUN mkdir /app
RUN mkdir /conf

COPY . /app
RUN apt install -y python
RUN apt install -y python-pip
RUN pip install Jinja2

WORKDIR /app 

CMD python /app/init.py > /conf/oc-agent-config.yaml


