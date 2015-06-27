FROM python:2.7
ADD . /src
RUN cd /src && pip install -r requirements.txt
WORKDIR /src
