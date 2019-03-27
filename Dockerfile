FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
RUN apk add --update bash
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/