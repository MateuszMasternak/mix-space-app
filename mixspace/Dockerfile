FROM python:3.11

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
